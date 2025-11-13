# Delete all Cloud Run services in a project
# Usage: .\delete-all-cloud-run.ps1 [project-id]

param(
    [string]$ProjectId = $env:GCP_PROJECT_ID,
    [string]$Region = "us-central1"
)

if (-not $ProjectId) {
    Write-Host "Usage: .\delete-all-cloud-run.ps1 <project-id> [region]" -ForegroundColor Red
    exit 1
}

Write-Host "⚠️  WARNING: This will delete ALL Cloud Run services!" -ForegroundColor Red
Write-Host "Project: $ProjectId" -ForegroundColor Yellow
Write-Host "Region: $Region" -ForegroundColor Yellow

$confirmation = Read-Host "`nType 'yes' to confirm"

if ($confirmation -ne 'yes') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nListing services..." -ForegroundColor Cyan
$services = gcloud run services list --platform=managed --region=$Region --project=$ProjectId --format="value(metadata.name)"

if (-not $services) {
    Write-Host "No services found." -ForegroundColor Green
    exit 0
}

foreach ($service in $services) {
    Write-Host "Deleting: $service" -ForegroundColor Yellow
    gcloud run services delete $service --region=$Region --project=$ProjectId --quiet
}

Write-Host "`n✅ All Cloud Run services deleted." -ForegroundColor Green

