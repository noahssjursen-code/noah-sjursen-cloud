# Cloud Run Deployment - Standard Pattern

## Deployment Requirements

### Procfile (Optional)

For buildpack deployments:

```
web: python api/main.py
```

### Dockerfile (If needed)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY api/ ./api/
COPY dashboard/build/ ./dashboard/build/

# Run
CMD ["python", "api/main.py"]
```

### Port Configuration

Always use `PORT` environment variable:

```python
port = int(os.environ.get("PORT", 8080))
uvicorn.run(app, host="0.0.0.0", port=port)
```

Cloud Run sets `PORT` automatically.

## Deploy Script Pattern

```powershell
# deploy.ps1
$PROJECT_ID = "your-project-id"
$SERVICE_NAME = "service-name"
$REGION = "us-central1"

Write-Host "Deploying to Cloud Run..." -ForegroundColor Green

gcloud run deploy $SERVICE_NAME `
    --source . `
    --region=$REGION `
    --platform=managed `
    --allow-unauthenticated `
    --project=$PROJECT_ID

Write-Host "Deployed!" -ForegroundColor Green
```

## Environment Variables

Set in Cloud Run:

```powershell
gcloud run services update $SERVICE_NAME `
    --set-env-vars="ENVIRONMENT=production,API_KEY=value" `
    --region=$REGION `
    --project=$PROJECT_ID
```

Or use `.env` file locally (git-ignored).

## Service Account (If needed)

```powershell
# Create service account
gcloud iam service-accounts create $SERVICE_NAME-sa `
    --project=$PROJECT_ID

# Assign to service
gcloud run services update $SERVICE_NAME `
    --service-account=$SERVICE_NAME-sa@$PROJECT_ID.iam.gserviceaccount.com `
    --region=$REGION `
    --project=$PROJECT_ID
```

## VPC Connector (For internal resources)

```powershell
gcloud run services update $SERVICE_NAME `
    --vpc-connector=vpc-connector-name `
    --vpc-egress=private-ranges-only `
    --region=$REGION `
    --project=$PROJECT_ID
```

## Memory and CPU

```powershell
gcloud run deploy $SERVICE_NAME `
    --memory=512Mi `
    --cpu=1 `
    --min-instances=0 `
    --max-instances=10 `
    --region=$REGION `
    --project=$PROJECT_ID
```

## Health Checks

Cloud Run uses `/` by default. Add health endpoint:

```python
@app.get("/api/health")
def health():
    return {"status": "healthy"}
```

## Building Process

Cloud Run builds automatically from source:

1. Detects `requirements.txt` and `Procfile`
2. Installs dependencies
3. Builds container
4. Deploys

## Testing Deployment

```powershell
# Get service URL
$URL = gcloud run services describe $SERVICE_NAME `
    --region=$REGION `
    --format="value(status.url)" `
    --project=$PROJECT_ID

# Test
Invoke-WebRequest "$URL/api/health"
```

## Logs

```powershell
gcloud run services logs read $SERVICE_NAME `
    --region=$REGION `
    --project=$PROJECT_ID `
    --limit=50
```

## Authentication

### Allow Unauthenticated (Public)

```powershell
gcloud run services add-iam-policy-binding $SERVICE_NAME `
    --member="allUsers" `
    --role="roles/run.invoker" `
    --region=$REGION `
    --project=$PROJECT_ID
```

### Require Authentication

Don't add `allUsers` binding. Only authenticated requests allowed.

## Docker Best Practices

- Use slim base images (`python:3.11-slim`)
- Copy only what's needed
- Use `.dockerignore` to exclude unnecessary files
- Don't run as root (add `USER` directive if needed)

## .dockerignore

```
node_modules/
__pycache__/
*.pyc
.git/
.env
.vscode/
dashboard/src/
venv/
```

## Common Issues

### Port Binding

Always bind to `0.0.0.0`, not `localhost`:

```python
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Build Timeout

Increase timeout:

```powershell
gcloud run deploy --timeout=900
```

### Memory Issues

Increase memory:

```powershell
gcloud run deploy --memory=1Gi
```

