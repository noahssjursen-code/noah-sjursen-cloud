# Setup Redis Server on GCP
# Uses free-tier e2-micro instance

$PROJECT_ID = "noah-sjursen-cloud"
$ZONE = "us-central1-a"
$INSTANCE_NAME = "redis-server"

Write-Host "Creating Redis server on GCP..." -ForegroundColor Green

# Create temporary startup script file
$STARTUP_SCRIPT_FILE = Join-Path $env:TEMP "redis-startup.sh"
@'
#!/bin/bash
apt-get update
apt-get install -y redis-server

# Create proper Redis config
cat > /etc/redis/redis.conf <<'REDISEOF'
bind 0.0.0.0
port 6379
daemonize no
supervised systemd
protected-mode no
maxmemory 768mb
maxmemory-policy allkeys-lru
dir /var/lib/redis
REDISEOF

systemctl restart redis-server
systemctl enable redis-server
echo "Redis setup complete!"
'@ | Out-File -FilePath $STARTUP_SCRIPT_FILE -Encoding UTF8

# Create the instance
Write-Host "`nCreating e2-micro instance..." -ForegroundColor Yellow
gcloud compute instances create $INSTANCE_NAME `
    --project=$PROJECT_ID `
    --zone=$ZONE `
    --machine-type=e2-micro `
    --image-family=debian-12 `
    --image-project=debian-cloud `
    --boot-disk-size=10GB `
    --boot-disk-type=pd-standard `
    --tags=redis-server `
    --metadata-from-file=startup-script=$STARTUP_SCRIPT_FILE

# Clean up temp file
Remove-Item $STARTUP_SCRIPT_FILE -ErrorAction SilentlyContinue

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nFailed to create instance!" -ForegroundColor Red
    exit 1
}

# Create firewall rule for internal access
Write-Host "`nCreating firewall rule for internal Redis access..." -ForegroundColor Yellow
gcloud compute firewall-rules create allow-redis-internal `
    --project=$PROJECT_ID `
    --allow=tcp:6379 `
    --source-ranges=10.128.0.0/9 `
    --target-tags=redis-server `
    --description="Allow internal VPC access to Redis"

if ($LASTEXITCODE -ne 0) {
    Write-Host "`nNote: Firewall rule may already exist (this is OK)" -ForegroundColor Yellow
}

# Wait a moment for instance to initialize
Write-Host "`nWaiting for instance to start..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Get the internal IP
Write-Host "`nGetting Redis server IP..." -ForegroundColor Yellow
$REDIS_IP = gcloud compute instances describe $INSTANCE_NAME --zone=$ZONE --format="get(networkInterfaces[0].networkIP)"

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Redis Server Created Successfully!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nInternal IP: $REDIS_IP" -ForegroundColor Cyan
Write-Host "Port: 6379" -ForegroundColor Cyan
Write-Host "Connection string: redis://${REDIS_IP}:6379" -ForegroundColor Cyan
Write-Host "`nUse this IP in your Cloud Run services to connect." -ForegroundColor Yellow
Write-Host "`nRedis is installing in the background (takes ~2 minutes)" -ForegroundColor Yellow
Write-Host "`nTo test connection:" -ForegroundColor White
Write-Host "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='redis-cli ping'" -ForegroundColor Gray
Write-Host "`nTo view logs:" -ForegroundColor White
Write-Host "  gcloud compute ssh $INSTANCE_NAME --zone=$ZONE --command='tail -f /var/log/redis/redis-server.log'" -ForegroundColor Gray
Write-Host ""

