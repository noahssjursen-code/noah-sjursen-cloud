"""
Cloud Control Center - GCP Management Dashboard
FastAPI backend with SvelteKit frontend
"""

import sys
import os

# Add parent directories to path for reusables
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))
sys.path.insert(0, os.path.dirname(__file__))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="Cloud Control Center",
    description="GCP resource management dashboard",
    version="0.1.0",
    docs_url="/api/docs"
)


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


# Mount dashboard (after all API routes)
dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'build')
if os.path.exists(dashboard_path):
    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    
    print("\n" + "=" * 50)
    print("🎛️  Starting Cloud Control Center...")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=port)

