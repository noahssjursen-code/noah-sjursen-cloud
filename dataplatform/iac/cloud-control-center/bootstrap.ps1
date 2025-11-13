# Bootstrap Cloud Control Center Infrastructure
# Runs all setup scripts in sequence

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID,
    [switch]$OAuth,
    [switch]$ServiceAccount
)

if (-not $ProjectId) {
    Write-Host "Usage: .\bootstrap.ps1 <project-id> [-OAuth] [-ServiceAccount]" -ForegroundColor Red
    Write-Host "`nOptions:" -ForegroundColor Yellow
    Write-Host "  -OAuth           Setup OAuth authentication" -ForegroundColor Gray
    Write-Host "  -ServiceAccount  Setup Service Account authentication" -ForegroundColor Gray
    Write-Host "`nExample:" -ForegroundColor Yellow
    Write-Host "  .\bootstrap.ps1 my-project -ServiceAccount" -ForegroundColor Gray
    exit 1
}

if (-not $OAuth -and -not $ServiceAccount) {
    Write-Host "Error: Specify -OAuth or -ServiceAccount (or both)" -ForegroundColor Red
    exit 1
}

Write-Host "Bootstrapping Cloud Control Center Infrastructure" -ForegroundColor Cyan
Write-Host "Project: $ProjectId`n" -ForegroundColor Yellow

$failed = $false

# Setup Service Account (if requested)
if ($ServiceAccount) {
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Step 1: Setting up Service Account" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    .\setup-service-account.ps1 $ProjectId
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nFailed: Service Account setup" -ForegroundColor Red
        $failed = $true
    }
}

# Setup OAuth (if requested)
if ($OAuth) {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "Step 2: Setting up OAuth 2.0" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
    
    .\setup-oauth.ps1 $ProjectId
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "`nFailed: OAuth setup" -ForegroundColor Red
        $failed = $true
    }
}

if ($failed) {
    Write-Host "`n❌ Bootstrap completed with errors" -ForegroundColor Red
    exit 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "✅ Cloud Control Center Bootstrap Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor White
Write-Host "  1. Add credentials to cloud-control-center/.env" -ForegroundColor Gray
Write-Host "  2. Run the application: cd ../../projects/cloud-control-center && .\startNbuild.ps1" -ForegroundColor Gray
Write-Host ""

