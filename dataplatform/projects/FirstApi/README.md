# FirstApi

A simple test API for Noah Sjursen Cloud demonstrating:
- ✅ Cloud Run source-based deployment (no Docker!)
- ✅ Shared reusables pattern (like C# class libraries)
- ✅ FastAPI framework

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Test endpoints
curl http://localhost:8080/
curl http://localhost:8080/info
curl http://localhost:8080/health
```

## Deploy to GCP

1. Edit `deploy.sh` and set your `PROJECT_ID`
2. Make sure you're authenticated: `gcloud auth login`
3. Run deployment:

```bash
# On Linux/Mac
chmod +x deploy.sh
./deploy.sh

# On Windows (PowerShell)
bash deploy.sh
```

## Endpoints

- `GET /` - Root endpoint with greeting from reusables
- `GET /info` - API and reusables library information
- `GET /health` - Health check
- `GET /docs` - Auto-generated API documentation (FastAPI feature!)

## How it works

This API imports shared utilities from the `reusables/` folder, demonstrating the same pattern you use at work with C# class libraries and TableStorage clients.

The `deploy.sh` script copies the reusables folder during deployment, so all shared code is available to the Cloud Run service.

