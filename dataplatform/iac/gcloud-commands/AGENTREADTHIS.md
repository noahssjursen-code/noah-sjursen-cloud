# GCloud Commands Reference

## Purpose

Reusable gcloud CLI commands organized by category. Store frequently used commands here for quick reference and reuse.

**Note:** This is a command library, not an IaC component. No bootstrap script needed.

## File Naming

Use descriptive names:

- `list-services.sh` / `list-services.ps1`
- `delete-all-resources.sh` / `delete-all-resources.ps1`
- `setup-iam.sh` / `setup-iam.ps1`

## Command File Pattern

### PowerShell

```powershell
# Description of what this does
# Usage: .\script.ps1 <args>

$PROJECT_ID = "project-id"

gcloud command `
    --flag=value `
    --project=$PROJECT_ID
```

### Bash/Shell

```bash
#!/bin/bash
# Description of what this does
# Usage: ./script.sh <args>

PROJECT_ID="project-id"

gcloud command \
    --flag=value \
    --project=$PROJECT_ID
```

## Categories

Organize commands by what they do:

- **List/Query** - Get information
- **Create/Setup** - Create resources
- **Delete/Cleanup** - Remove resources
- **Update** - Modify resources
- **IAM** - Permissions and service accounts

## Variables

Always parameterize:

```powershell
$PROJECT_ID = $args[0]
if (-not $PROJECT_ID) {
    Write-Host "Usage: .\script.ps1 <project-id>"
    exit 1
}
```

Or use environment variables:

```powershell
$PROJECT_ID = $env:GCP_PROJECT_ID
if (-not $PROJECT_ID) {
    $PROJECT_ID = "default-project"
}
```

## Output Formatting

Use `--format` for structured output:

```powershell
# JSON
gcloud run services list --format=json

# Table
gcloud compute instances list --format="table(name,zone,status)"

# Value (single field)
gcloud run services describe service-name --format="value(status.url)"
```

## Common Commands to Store

- List all running services across all regions
- List all resources (compute, run, storage, etc.)
- Estimate current costs
- Delete all resources in project
- Setup IAM roles
- Create/delete service accounts
- Configure VPC
- Enable/disable APIs

