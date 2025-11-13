# Setup custom IAM roles for Cloud Control Center
# Creates application-specific roles with defined permissions

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID
)

if (-not $ProjectId) {
    Write-Host "Usage: .\setup-custom-roles.ps1 <project-id>" -ForegroundColor Red
    exit 1
}

Write-Host "Creating custom IAM roles for Cloud Control Center" -ForegroundColor Cyan
Write-Host "Project: $ProjectId" -ForegroundColor Yellow
Write-Host ""

# Define custom roles
$roles = @(
    @{
        Name = "cloudControlCenterViewer"
        Title = "Cloud Control Center Viewer"
        Description = "Read-only access to view resources in Cloud Control Center"
        Permissions = @(
            "compute.instances.list",
            "compute.instances.get",
            "run.services.list",
            "run.services.get",
            "storage.buckets.list",
            "storage.buckets.get",
            "resourcemanager.projects.get"
        )
    },
    @{
        Name = "cloudControlCenterOperator"
        Title = "Cloud Control Center Operator"
        Description = "Can view and manage resources via Cloud Control Center"
        Permissions = @(
            "compute.instances.list",
            "compute.instances.get",
            "compute.instances.start",
            "compute.instances.stop",
            "run.services.list",
            "run.services.get",
            "run.services.update",
            "storage.buckets.list",
            "storage.buckets.get",
            "resourcemanager.projects.get",
            "iam.roles.list",
            "iam.serviceAccounts.list"
        )
    },
    @{
        Name = "cloudControlCenterAdmin"
        Title = "Cloud Control Center Admin"
        Description = "Full administrative access to Cloud Control Center"
        Permissions = @(
            "compute.instances.list",
            "compute.instances.get",
            "compute.instances.start",
            "compute.instances.stop",
            "compute.instances.delete",
            "compute.instances.create",
            "run.services.list",
            "run.services.get",
            "run.services.update",
            "run.services.delete",
            "run.services.create",
            "storage.buckets.list",
            "storage.buckets.get",
            "storage.buckets.delete",
            "storage.buckets.create",
            "resourcemanager.projects.get",
            "iam.roles.list",
            "iam.roles.get",
            "iam.roles.create",
            "iam.roles.update",
            "iam.roles.delete",
            "iam.serviceAccounts.list",
            "iam.serviceAccounts.get",
            "iam.serviceAccounts.create",
            "iam.serviceAccounts.delete"
        )
    }
)

foreach ($role in $roles) {
    Write-Host "Creating role: $($role.Name)" -ForegroundColor Yellow
    
    # Create temporary YAML file for role definition
    $yamlFile = [System.IO.Path]::GetTempFileName()
    $yamlContent = @"
title: $($role.Title)
description: $($role.Description)
stage: GA
includedPermissions:
"@
    
    foreach ($perm in $role.Permissions) {
        $yamlContent += "`n- $perm"
    }
    
    [System.IO.File]::WriteAllText($yamlFile, $yamlContent)
    
    # Create the role
    $createResult = gcloud iam roles create $($role.Name) `
        --project=$ProjectId `
        --file=$yamlFile 2>&1
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  Created $($role.Name)" -ForegroundColor Green
    } else {
        if ($createResult -like "*already exists*") {
            Write-Host "  Role already exists: $($role.Name)" -ForegroundColor Gray
        } else {
            Write-Host "  Failed to create $($role.Name): $createResult" -ForegroundColor Red
        }
    }
    
    Remove-Item $yamlFile -ErrorAction SilentlyContinue
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host "Custom Roles Created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Available roles:" -ForegroundColor White
Write-Host "  - projects/$ProjectId/roles/cloudControlCenterViewer" -ForegroundColor Cyan
Write-Host "  - projects/$ProjectId/roles/cloudControlCenterOperator" -ForegroundColor Cyan
Write-Host "  - projects/$ProjectId/roles/cloudControlCenterAdmin" -ForegroundColor Cyan
Write-Host ""
Write-Host "To assign a role:" -ForegroundColor White
Write-Host "  .\assign-role.ps1 $ProjectId user@gmail.com viewer" -ForegroundColor Gray
Write-Host ""

