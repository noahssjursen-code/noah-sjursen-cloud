# Setup VPC Connector for Cloud Run to access Redis
# Allows Cloud Run services to reach internal VPC resources

$PROJECT_ID = "noah-sjursen-cloud"
$REGION = "us-central1"
$CONNECTOR_NAME = "redis-connector"

Write-Host "Creating VPC Connector for Cloud Run..." -ForegroundColor Green

# Enable VPC Access API
Write-Host "`nEnabling VPC Access API..." -ForegroundColor Yellow
gcloud services enable vpcaccess.googleapis.com --project=$PROJECT_ID

# Create VPC Connector
Write-Host "`nCreating VPC connector..." -ForegroundColor Yellow
gcloud compute networks vpc-access connectors create $CONNECTOR_NAME `
    --region=$REGION `
    --network=default `
    --range=10.8.0.0/28 `
    --min-instances=2 `
    --max-instances=3 `
    --machine-type=e2-micro `
    --project=$PROJECT_ID

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "VPC Connector Created Successfully!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nConnector: $CONNECTOR_NAME" -ForegroundColor Cyan
    Write-Host "Region: $REGION" -ForegroundColor Cyan
    Write-Host "`nYour Cloud Run services can now reach Redis at 10.128.0.3" -ForegroundColor Yellow
    Write-Host "`nDeploy services with:" -ForegroundColor White
    Write-Host "  --vpc-connector=$CONNECTOR_NAME" -ForegroundColor Gray
    Write-Host "  --vpc-egress=private-ranges-only" -ForegroundColor Gray
} else {
    Write-Host "`nFailed to create VPC connector!" -ForegroundColor Red
}

