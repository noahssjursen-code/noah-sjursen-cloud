# Infrastructure as Code (IaC)

## Purpose

All GCP infrastructure automation using PowerShell + gcloud CLI. Simple, reproducible, no Terraform complexity.

## Structure Pattern

Each infrastructure component gets its own folder:

```
iac/
├── AGENTREADTHIS.md          # This file
├── <component-name>/         # One folder per component
│   ├── AGENTREADTHIS.md      # Component-specific docs
│   ├── bootstrap.ps1         # Run all setup in sequence
│   ├── setup-*.ps1           # Setup scripts
│   ├── destroy-*.ps1         # Teardown scripts
│   └── .gitignore            # Protect secrets/keys
└── gcloud-commands/          # Reusable command library
```

## Component Folder Pattern

### Required Files

**`AGENTREADTHIS.md`**
- What this component does
- What resources it creates
- Prerequisites
- Usage instructions
- Security notes

**`bootstrap.ps1`**
- Runs all setup scripts in correct sequence
- Accepts project ID parameter
- Idempotent (safe to run multiple times)
- Outputs configuration for .env files

**`setup-*.ps1`**
- Individual setup scripts for specific resources
- Accept parameters (project ID, region, etc.)
- Enable required APIs
- Create resources
- Output connection strings/credentials

**`destroy-*.ps1`**
- Teardown scripts matching each setup script
- Prompt for confirmation
- Delete resources safely

**`.gitignore`**
- Protect service account keys
- Protect .env files
- Protect any sensitive outputs

### Optional Files

**`README.md`**
- User-friendly documentation
- Quick start guide

**`verify-*.ps1`**
- Test that setup worked
- Verify connectivity
- Check permissions

## Naming Conventions

### Folders
- Lowercase with hyphens: `cloud-control-center`, `redis-cache`, `vpc-networking`
- Descriptive of what it manages

### Scripts
- `bootstrap.ps1` - Main orchestrator
- `setup-<resource>.ps1` - Create specific resource
- `destroy-<resource>.ps1` - Delete specific resource
- `verify-<resource>.ps1` - Test specific resource

### Parameters
Always accept project ID as first parameter with environment variable fallback:

```powershell
param(
    [string]$ProjectId = $env:GCP_PROJECT_ID
)

if (-not $ProjectId) {
    Write-Host "Usage: .\script.ps1 <project-id>" -ForegroundColor Red
    exit 1
}
```

## Bootstrap Script Pattern

Every component folder has a `bootstrap.ps1` that runs everything:

```powershell
# Bootstrap <Component Name>
# Runs all setup scripts in sequence

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID
)

if (-not $ProjectId) {
    Write-Host "Usage: .\bootstrap.ps1 <project-id>" -ForegroundColor Red
    exit 1
}

Write-Host "Bootstrapping <Component>..." -ForegroundColor Cyan
Write-Host "Project: $ProjectId`n" -ForegroundColor Yellow

# Step 1: Setup first resource
Write-Host "Step 1: Setting up X..." -ForegroundColor Yellow
.\setup-x.ps1 $ProjectId

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed at step 1" -ForegroundColor Red
    exit 1
}

# Step 2: Setup second resource
Write-Host "`nStep 2: Setting up Y..." -ForegroundColor Yellow
.\setup-y.ps1 $ProjectId

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed at step 2" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "<Component> Bootstrap Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor White
Write-Host "  1. Add credentials to .env" -ForegroundColor Gray
Write-Host "  2. Run verification script" -ForegroundColor Gray
```

## Script Output Format

All scripts should output:
1. What they're doing (colored output)
2. Success/failure status
3. Configuration values (for .env files)
4. Next steps

Use color coding:
- **Cyan**: Headers/titles
- **Yellow**: Actions in progress
- **Green**: Success messages
- **Red**: Errors
- **Gray**: Supporting info

## API Management

Scripts should enable required APIs automatically:

```powershell
Write-Host "Enabling required APIs..." -ForegroundColor Yellow
$apis = @(
    "compute.googleapis.com",
    "run.googleapis.com"
)

foreach ($api in $apis) {
    Write-Host "  - $api"
    gcloud services enable $api --project=$ProjectId
}
```

## Security Practices

### .gitignore Requirements

Every component folder must have:

```
# Service account keys
*-sa-key.json
*.json

# Environment files
.env

# Terraform state (if ever used)
*.tfstate
*.tfstate.backup
```

### Key Management

- Never commit service account keys
- Output key locations in setup scripts
- Provide .env examples, not actual .env files
- Document key rotation process

## Current Components

### `cloud-control-center/`
Authentication and permissions for Cloud Control Center dashboard.

**Resources:**
- OAuth 2.0 client configuration
- Service account with viewer permissions

**Bootstrap:** `.\bootstrap.ps1 <project-id>`

### `gcloud-commands/`
Library of reusable gcloud CLI commands for reference.

**Not infrastructure** - just command reference scripts.

## Adding New Components

When adding new infrastructure:

1. Create folder: `iac/<component-name>/`
2. Add `AGENTREADTHIS.md` explaining what it does
3. Create setup scripts: `setup-*.ps1`
4. Create `bootstrap.ps1` to orchestrate setup
5. Create destroy scripts: `destroy-*.ps1`
6. Add `.gitignore` to protect secrets
7. Document environment variables needed
8. Test bootstrap process on fresh project

## Philosophy

- **Simple over complex** - PowerShell + gcloud, not Terraform
- **Idempotent** - Safe to run multiple times
- **Transparent** - Show what's happening
- **Portable** - Works on any GCP project
- **Documented** - Every component self-documenting

