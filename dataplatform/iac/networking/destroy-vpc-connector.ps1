# Destroy VPC Connector
# ⚠️ WARNING: Cloud Run services using this connector will lose VPC access!

$PROJECT_ID = "noah-sjursen-cloud"
$REGION = "us-central1"
$CONNECTOR_NAME = "redis-connector"

Write-Host "⚠️  WARNING: This will DELETE the VPC connector!" -ForegroundColor Red
Write-Host "Cloud Run services will lose access to internal resources (Redis)" -ForegroundColor Yellow
$confirmation = Read-Host "Type 'yes' to confirm"

if ($confirmation -ne 'yes') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nDeleting VPC connector..." -ForegroundColor Yellow
gcloud compute networks vpc-access connectors delete $CONNECTOR_NAME `
    --region=$REGION `
    --project=$PROJECT_ID `
    --quiet

Write-Host "`n✅ VPC connector destroyed." -ForegroundColor Green

