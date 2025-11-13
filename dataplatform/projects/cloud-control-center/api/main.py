"""
Cloud Control Center - GCP Management Dashboard
FastAPI backend with SvelteKit frontend
"""

import sys
import os

# Add parent directories to path for reusables
reusables_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
sys.path.insert(0, reusables_path)
sys.path.insert(0, os.path.dirname(__file__))

print(f"Reusables path: {reusables_path}")

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from pydantic import BaseModel
from auth import oauth, SESSION_SECRET
from reusables.python.gcp import (
    check_user_has_project_access, 
    list_all_resources, 
    get_user_role_level,
    list_project_iam_members,
    assign_role_to_user,
    revoke_role_from_user
)

app = FastAPI(
    title="Cloud Control Center",
    description="GCP resource management dashboard",
    version="0.1.0",
    docs_url="/api/docs"
)

# Add session middleware
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)


# Pydantic models for request bodies
class RoleAssignmentRequest(BaseModel):
    email: str
    role: str  # viewer, operator, or admin


@app.get("/api")
def root():
    """API root endpoint."""
    return {
        "service": "Cloud Control Center",
        "version": "0.1.0",
        "description": "GCP management dashboard"
    }


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/api/resources")
async def get_resources(request: Request):
    """Get all GCP resources for the project."""
    user = request.session.get('user')
    if not user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
    
    try:
        resources = list_all_resources(project_id)
        return {
            "success": True,
            "project_id": project_id,
            "resources": resources,
            "counts": {
                "compute_instances": len(resources.get('compute_instances', [])),
                "cloud_run_services": len(resources.get('cloud_run_services', [])),
                "storage_buckets": len(resources.get('storage_buckets', []))
            }
        }
    except Exception as e:
        return JSONResponse(
            {"success": False, "error": str(e)},
            status_code=500
        )


@app.get("/auth/login")
async def login(request: Request):
    """Redirect to Google OAuth login."""
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@app.get("/auth/callback")
async def auth_callback(request: Request):
    """Handle OAuth callback from Google."""
    token = await oauth.google.authorize_access_token(request)
    user = token.get('userinfo')
    
    if user:
        email = user.get('email', '')
        project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
        
        # Check if user has IAM access to GCP project
        if not check_user_has_project_access(email, project_id):
            return RedirectResponse(url='/?error=unauthorized')
        
        request.session['user'] = dict(user)
    
    return RedirectResponse(url='/')


@app.get("/auth/logout")
async def logout(request: Request):
    """Logout user."""
    request.session.clear()
    return RedirectResponse(url='/')


@app.get("/api/user")
async def get_user(request: Request):
    """Get current logged-in user with role level."""
    user = request.session.get('user')
    if not user:
        return JSONResponse({"authenticated": False}, status_code=401)
    
    # Get user's role level
    email = user.get('email', '')
    project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
    role_level = get_user_role_level(email, project_id)
    
    return {
        "authenticated": True,
        "email": user.get('email'),
        "name": user.get('name'),
        "picture": user.get('picture'),
        "role": role_level
    }


@app.get("/api/users")
async def get_users(request: Request):
    """Get all users with Cloud Control Center roles."""
    user = request.session.get('user')
    if not user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    # Check if user has access
    email = user.get('email', '')
    project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
    
    if not check_user_has_project_access(email, project_id):
        return JSONResponse({"error": "Unauthorized"}, status_code=403)
    
    # Get user's role - only admins can view all users
    role_level = get_user_role_level(email, project_id)
    if role_level != 'admin':
        return JSONResponse({"error": "Admin access required"}, status_code=403)
    
    try:
        # Get all users with Cloud Control Center roles
        users = list_project_iam_members(project_id, filter_cloud_control_only=True)
        return {"users": users}
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/users/assign-role")
async def assign_role(request: Request, assignment: RoleAssignmentRequest):
    """Assign a Cloud Control Center role to a user."""
    user = request.session.get('user')
    if not user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    # Check if user has admin access
    email = user.get('email', '')
    project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
    role_level = get_user_role_level(email, project_id)
    
    if role_level != 'admin':
        return JSONResponse({"error": "Admin access required"}, status_code=403)
    
    try:
        result = assign_role_to_user(assignment.email, assignment.role, project_id)
        if result['success']:
            return {"success": True, "message": result['message']}
        else:
            return JSONResponse({"error": result['message']}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/api/users/revoke-role")
async def revoke_role(request: Request, assignment: RoleAssignmentRequest):
    """Revoke a Cloud Control Center role from a user."""
    user = request.session.get('user')
    if not user:
        return JSONResponse({"error": "Not authenticated"}, status_code=401)
    
    # Check if user has admin access
    email = user.get('email', '')
    project_id = os.getenv('GCP_PROJECT_ID', 'noah-sjursen-cloud')
    role_level = get_user_role_level(email, project_id)
    
    if role_level != 'admin':
        return JSONResponse({"error": "Admin access required"}, status_code=403)
    
    try:
        result = revoke_role_from_user(assignment.email, assignment.role, project_id)
        if result['success']:
            return {"success": True, "message": result['message']}
        else:
            return JSONResponse({"error": result['message']}, status_code=400)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


# Mount dashboard (after all API routes)
dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'build')
if os.path.exists(dashboard_path):
    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    
    print("\n" + "=" * 50)
    print("Starting Cloud Control Center...")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=port)

