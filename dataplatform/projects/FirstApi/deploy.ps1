# Deploy FirstApi to Google Cloud Run
# Uses source-based deployment (no Dockerfile needed!)

# Configuration
$SERVICE_NAME = "firstapi"
$REGION = "us-central1"
$PROJECT_ID = "noah-sjursen-cloud"
$VPC_CONNECTOR = "redis-connector"

Write-Host "Deploying FirstApi to Cloud Run..." -ForegroundColor Green
Write-Host "Service: $SERVICE_NAME"
Write-Host "Region: $REGION"
Write-Host "VPC Connector: $VPC_CONNECTOR (for Redis access)" -ForegroundColor Cyan

# Copy reusables into the project for deployment
Write-Host "`nCopying reusables library..." -ForegroundColor Yellow
Copy-Item -Path ..\reusables -Destination .\reusables -Recurse -Force

try {
    # Deploy to Cloud Run (source-based deployment)
    Write-Host "`nDeploying to Cloud Run..." -ForegroundColor Yellow
    gcloud run deploy $SERVICE_NAME `
        --source . `
        --region $REGION `
        --platform managed `
        --allow-unauthenticated `
        --project $PROJECT_ID `
        --max-instances 10 `
        --memory 256Mi `
        --vpc-connector=$VPC_CONNECTOR `
        --vpc-egress=private-ranges-only `
        --set-env-vars="ENVIRONMENT=production"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n========================================" -ForegroundColor Green
        Write-Host "Deployment Complete!" -ForegroundColor Green
        Write-Host "========================================" -ForegroundColor Green
        Write-Host "`nYour API is now connected to Redis!" -ForegroundColor Cyan
        Write-Host "The API uses internal IP (10.128.0.3) for Redis access." -ForegroundColor Yellow
    } else {
        Write-Host "`nDeployment failed!" -ForegroundColor Red
        Write-Host "If VPC connector doesn't exist, run: dataplatform/iac/networking/setup-vpc-connector.ps1" -ForegroundColor Yellow
    }
}
finally {
    # Clean up copied reusables (always runs, even if deployment fails)
    Write-Host "`nCleaning up..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force reusables -ErrorAction SilentlyContinue
    Write-Host "Done!" -ForegroundColor Green
}

