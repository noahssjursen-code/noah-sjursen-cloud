# Destroy Redis Server on GCP
# ⚠️ WARNING: This will delete all data in Redis!

$PROJECT_ID = "noah-sjursen-cloud"
$ZONE = "us-central1-a"
$INSTANCE_NAME = "redis-server"

Write-Host "⚠️  WARNING: This will DELETE the Redis server and ALL data!" -ForegroundColor Red
$confirmation = Read-Host "Type 'yes' to confirm"

if ($confirmation -ne 'yes') {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host "`nDeleting Redis server..." -ForegroundColor Yellow
gcloud compute instances delete $INSTANCE_NAME `
    --project=$PROJECT_ID `
    --zone=$ZONE `
    --quiet

Write-Host "`nDeleting firewall rule..." -ForegroundColor Yellow
gcloud compute firewall-rules delete allow-redis-internal `
    --project=$PROJECT_ID `
    --quiet

Write-Host "`n✅ Redis server destroyed." -ForegroundColor Green

