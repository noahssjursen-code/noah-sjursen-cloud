# Revoke Cloud Control Center role from a user
# Usage: .\revoke-role.ps1 <project-id> <email> <viewer|operator|admin>

param(
    [string]$ProjectId,
    [string]$Email,
    [string]$RoleLevel
)

if (-not $ProjectId -or -not $Email -or -not $RoleLevel) {
    Write-Host "Usage: .\revoke-role.ps1 <project-id> <email> <viewer|operator|admin>" -ForegroundColor Red
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\revoke-role.ps1 my-project user@gmail.com viewer" -ForegroundColor Gray
    Write-Host "  .\revoke-role.ps1 my-project admin@gmail.com admin" -ForegroundColor Gray
    Write-Host ""
    Write-Host "To revoke ALL Cloud Control Center roles:" -ForegroundColor Yellow
    Write-Host "  .\revoke-role.ps1 my-project user@gmail.com all" -ForegroundColor Gray
    exit 1
}

# Map role level to full role name
$roleMap = @{
    "viewer" = "cloudControlCenterViewer"
    "operator" = "cloudControlCenterOperator"
    "admin" = "cloudControlCenterAdmin"
}

Write-Host "Revoking role from user" -ForegroundColor Cyan
Write-Host "User: $Email" -ForegroundColor Yellow
Write-Host ""

if ($RoleLevel.ToLower() -eq "all") {
    # Revoke all Cloud Control Center roles
    foreach ($role in $roleMap.Values) {
        $fullRole = "projects/$ProjectId/roles/$role"
        Write-Host "Revoking: $role" -ForegroundColor Yellow
        
        gcloud projects remove-iam-policy-binding $ProjectId `
            --member="user:$Email" `
            --role=$fullRole `
            --quiet 2>&1 | Out-Null
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "All Roles Revoked!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "$Email no longer has Cloud Control Center access" -ForegroundColor Cyan
    Write-Host ""
} else {
    $roleName = $roleMap[$RoleLevel.ToLower()]
    
    if (-not $roleName) {
        Write-Host "Error: Invalid role level. Use: viewer, operator, admin, or all" -ForegroundColor Red
        exit 1
    }
    
    $fullRole = "projects/$ProjectId/roles/$roleName"
    
    Write-Host "Role: $roleName" -ForegroundColor Yellow
    
    gcloud projects remove-iam-policy-binding $ProjectId `
        --member="user:$Email" `
        --role=$fullRole `
        --quiet
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host ""
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "Role Revoked Successfully!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host ""
        Write-Host "$Email no longer has $roleName access" -ForegroundColor Cyan
        Write-Host ""
    } else {
        Write-Host ""
        Write-Host "Failed to revoke role" -ForegroundColor Red
        Write-Host ""
    }
}

