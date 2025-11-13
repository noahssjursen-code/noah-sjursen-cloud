# Enable common GCP APIs
# Usage: .\enable-apis.ps1 [project-id]

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID
)

if (-not $ProjectId) {
    Write-Host "Usage: .\enable-apis.ps1 <project-id>" -ForegroundColor Red
    exit 1
}

Write-Host "Enabling APIs for project: $ProjectId`n" -ForegroundColor Cyan

$apis = @(
    "run.googleapis.com",              # Cloud Run
    "compute.googleapis.com",          # Compute Engine
    "vpcaccess.googleapis.com",        # VPC Access
    "cloudbuild.googleapis.com",       # Cloud Build
    "artifactregistry.googleapis.com", # Artifact Registry
    "storage.googleapis.com",          # Cloud Storage
    "iam.googleapis.com"               # IAM
)

foreach ($api in $apis) {
    Write-Host "Enabling: $api" -ForegroundColor Yellow
    gcloud services enable $api --project=$ProjectId
}

Write-Host "`n✅ All APIs enabled." -ForegroundColor Green

