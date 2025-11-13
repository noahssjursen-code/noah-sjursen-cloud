# List all active GCP resources
# Usage: .\list-all-resources.ps1 [project-id]

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID
)

if (-not $ProjectId) {
    Write-Host "Usage: .\list-all-resources.ps1 <project-id>" -ForegroundColor Red
    exit 1
}

Write-Host "Listing all resources in project: $ProjectId`n" -ForegroundColor Cyan

# Compute Engine instances
Write-Host "=== Compute Engine Instances ===" -ForegroundColor Yellow
gcloud compute instances list --project=$ProjectId

# Cloud Run services
Write-Host "`n=== Cloud Run Services ===" -ForegroundColor Yellow
gcloud run services list --platform=managed --project=$ProjectId

# Cloud Storage buckets
Write-Host "`n=== Cloud Storage Buckets ===" -ForegroundColor Yellow
gcloud storage buckets list --project=$ProjectId

# VPC Connectors
Write-Host "`n=== VPC Connectors ===" -ForegroundColor Yellow
gcloud compute networks vpc-access connectors list --project=$ProjectId 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "No VPC connectors or need to specify region" -ForegroundColor Gray
}

# Firewall rules
Write-Host "`n=== Firewall Rules ===" -ForegroundColor Yellow
gcloud compute firewall-rules list --project=$ProjectId

# Artifact Registry
Write-Host "`n=== Artifact Registry ===" -ForegroundColor Yellow
gcloud artifacts repositories list --project=$ProjectId

Write-Host "`nDone!" -ForegroundColor Green

