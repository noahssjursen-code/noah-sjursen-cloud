# Assign Cloud Control Center role to a user
# Usage: .\assign-role.ps1 <project-id> <email> <viewer|operator|admin>

param(
    [string]$ProjectId,
    [string]$Email,
    [string]$RoleLevel
)

if (-not $ProjectId -or -not $Email -or -not $RoleLevel) {
    Write-Host "Usage: .\assign-role.ps1 <project-id> <email> <viewer|operator|admin>" -ForegroundColor Red
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\assign-role.ps1 my-project user@gmail.com viewer" -ForegroundColor Gray
    Write-Host "  .\assign-role.ps1 my-project admin@gmail.com admin" -ForegroundColor Gray
    exit 1
}

# Map role level to full role name
$roleMap = @{
    "viewer" = "cloudControlCenterViewer"
    "operator" = "cloudControlCenterOperator"
    "admin" = "cloudControlCenterAdmin"
}

$roleName = $roleMap[$RoleLevel.ToLower()]

if (-not $roleName) {
    Write-Host "Error: Invalid role level. Use: viewer, operator, or admin" -ForegroundColor Red
    exit 1
}

$fullRole = "projects/$ProjectId/roles/$roleName"

Write-Host "Assigning role to user" -ForegroundColor Cyan
Write-Host "User: $Email" -ForegroundColor Yellow
Write-Host "Role: $roleName" -ForegroundColor Yellow
Write-Host ""

gcloud projects add-iam-policy-binding $ProjectId `
    --member="user:$Email" `
    --role=$fullRole `
    --quiet

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "Role Assigned Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "$Email now has $roleName access" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "Failed to assign role" -ForegroundColor Red
    Write-Host ""
}

