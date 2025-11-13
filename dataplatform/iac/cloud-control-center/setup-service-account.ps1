# Setup Service Account for Cloud Control Center
# Creates service account with permissions to manage GCP resources

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID,
    [string]$ServiceAccountName = "cloud-control-center"
)

if (-not $ProjectId) {
    Write-Host "Usage: .\setup-service-account.ps1 <project-id> [service-account-name]" -ForegroundColor Red
    exit 1
}

Write-Host "Setting up Service Account for Cloud Control Center" -ForegroundColor Cyan
Write-Host "Project: $ProjectId" -ForegroundColor Yellow
Write-Host "Service Account: $ServiceAccountName`n" -ForegroundColor Yellow

$serviceAccountEmail = "$ServiceAccountName@$ProjectId.iam.gserviceaccount.com"

# Create service account
Write-Host "Creating service account..." -ForegroundColor Yellow
gcloud iam service-accounts create $ServiceAccountName `
    --display-name="Cloud Control Center" `
    --description="Service account for Cloud Control Center operations" `
    --project=$ProjectId

if ($LASTEXITCODE -ne 0) {
    Write-Host "Note: Service account may already exist" -ForegroundColor Gray
}

# Grant roles
Write-Host "`nGranting IAM roles..." -ForegroundColor Yellow

$roles = @(
    "roles/viewer",                    # View all resources
    "roles/compute.viewer",            # View compute resources
    "roles/run.viewer",                # View Cloud Run services
    "roles/storage.objectViewer",      # View storage buckets
    "roles/logging.viewer"             # View logs
)

foreach ($role in $roles) {
    Write-Host "  - $role"
    gcloud projects add-iam-policy-binding $ProjectId `
        --member="serviceAccount:$serviceAccountEmail" `
        --role="$role" `
        --quiet | Out-Null
}

# Create key file
Write-Host "`nCreating service account key..." -ForegroundColor Yellow
$keyFile = "cloud-control-center-sa-key.json"

gcloud iam service-accounts keys create $keyFile `
    --iam-account=$serviceAccountEmail `
    --project=$ProjectId

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Service Account Created!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "Email: $serviceAccountEmail" -ForegroundColor Cyan
Write-Host "Key file: $keyFile" -ForegroundColor Cyan
Write-Host "`n⚠️  IMPORTANT: Keep the key file secure!" -ForegroundColor Red
Write-Host "Add to cloud-control-center/.env:" -ForegroundColor White
Write-Host "  GOOGLE_APPLICATION_CREDENTIALS=../../iac/cloud-control-center/$keyFile" -ForegroundColor Gray
Write-Host "`nAdd $keyFile to .gitignore!" -ForegroundColor Yellow
Write-Host ""

