# Cloud Control Center - TODO

## Future Features

### Custom RBAC Roles
Create application-specific IAM roles in GCP:

**Roles:**
- `roles/cloudControlCenter.viewer` - Read-only access
- `roles/cloudControlCenter.operator` - Execute commands
- `roles/cloudControlCenter.admin` - Full access

**Implementation:**
- Create IaC script: `iac/cloud-control-center/setup-custom-roles.ps1`
- Define granular permissions per role
- Update GCP reusable to check role levels
- Build admin UI for role management

**Command example:**
```powershell
gcloud iam roles create cloudControlCenterViewer \
  --project=noah-sjursen-cloud \
  --title="Cloud Control Center Viewer" \
  --permissions="compute.instances.list,run.services.list"
```

## Current Sprint

- [ ] Dashboard layout with left-hand menu
- [ ] Navigation: Overview, User Management, Applications (collapsible)

