# Deploy FirstApi to Google Cloud Run
# Uses source-based deployment (no Dockerfile needed!)

# Configuration
$SERVICE_NAME = "firstapi"
$REGION = "us-central1"
$PROJECT_ID = "noah-sjursen-cloud"

Write-Host "Deploying FirstApi to Cloud Run..." -ForegroundColor Green
Write-Host "Service: $SERVICE_NAME"
Write-Host "Region: $REGION"

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
        --memory 256Mi

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`nDeployment complete!" -ForegroundColor Green
        Write-Host "Your API should be available at the URL shown above." -ForegroundColor Green
    } else {
        Write-Host "`nDeployment failed!" -ForegroundColor Red
    }
}
finally {
    # Clean up copied reusables (always runs, even if deployment fails)
    Write-Host "`nCleaning up..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force reusables -ErrorAction SilentlyContinue
    Write-Host "Done!" -ForegroundColor Green
}

