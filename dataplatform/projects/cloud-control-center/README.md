# Cloud Control Center

Enterprise-grade GCP management dashboard with role-based access control, OAuth 2.0 authentication, and resource monitoring.

## Features

### Authentication & Authorization
- **Google OAuth 2.0** integration
- **Custom IAM roles** (Viewer, Operator, Admin)
- **Role-Based Access Control** (RBAC)
- Automatic permission checking via GCP IAM

### User Management (Admin Only)
- Assign Cloud Control Center roles to users
- Revoke roles from users
- View all users with access
- Real-time role updates

### Resource Monitoring
- **Compute Engine** instances
- **Cloud Run** services
- **Cloud Storage** buckets
- Real-time resource counts and status

### UI/UX
- Professional dark/light mode
- Responsive design with TailwindCSS
- Sidebar navigation
- Clean, modern interface

## Quick Start

### Initial Setup

1. **Set up OAuth credentials:**
```powershell
cd ../../iac/cloud-control-center
.\bootstrap.ps1 <project-id> -OAuth
```

2. **Create custom IAM roles:**
```powershell
.\bootstrap.ps1 <project-id> -CustomRoles
```

3. **Assign yourself admin access:**
```powershell
.\assign-role.ps1 <project-id> your-email@gmail.com admin
```

### Running Locally

**First time (or after code changes):**
```powershell
.\startNbuild.ps1
```

**Subsequent runs:**
```powershell
.\start.ps1
```

Opens on `http://localhost:8080`

## Architecture

```
cloud-control-center/
├── api/                    # FastAPI backend
│   ├── main.py            # API routes & OAuth
│   ├── auth.py            # Authentication logic
│   └── requirements.txt   # Python dependencies
├── dashboard/             # SvelteKit frontend
│   ├── src/
│   │   └── routes/
│   │       └── +page.svelte  # Main dashboard UI
│   └── package.json       # Node dependencies
└── .env                   # OAuth credentials (auto-generated)
```

## Custom IAM Roles

### Viewer
- View resources (Compute, Cloud Run, Storage)
- Read-only access to dashboard

### Operator
- All Viewer permissions
- Start/stop Compute instances
- Update Cloud Run services

### Admin
- All Operator permissions
- Manage user access
- Create/delete resources
- Full administrative control

## Tech Stack

- **Backend:** FastAPI + Uvicorn
- **Frontend:** SvelteKit + TypeScript + TailwindCSS
- **Authentication:** Google OAuth 2.0
- **Authorization:** GCP IAM with custom roles
- **Utilities:** Reusable GCP Python client
- **Deployment:** Cloud Run (future)

## Environment Variables

The `.env` file is auto-generated during OAuth setup and contains:
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `SESSION_SECRET`
- `GCP_PROJECT_ID`

## API Endpoints

- `GET /api/user` - Get authenticated user info
- `GET /api/resources` - List GCP resources
- `GET /api/users` - List users with access (admin only)
- `POST /api/users/assign-role` - Assign role (admin only)
- `POST /api/users/revoke-role` - Revoke role (admin only)
- `GET /auth/login` - OAuth login
- `GET /auth/callback` - OAuth callback
- `GET /auth/logout` - Logout

## Security

- OAuth 2.0 for authentication
- Session-based user management
- IAM-based authorization
- No hardcoded credentials
- Project-level role enforcement

## Development

See `AGENTREADTHIS-SVELTEKIT.md` and `AGENTREADTHIS-FASTAPI.md` in the parent directory for development patterns and guidelines.

