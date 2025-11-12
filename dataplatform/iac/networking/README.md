# Networking Infrastructure

VPC connectors and networking resources for Cloud Run services.

## VPC Connector

Allows Cloud Run services to access internal VPC resources (like Redis).

### Setup

```powershell
.\setup-vpc-connector.ps1
```

Creates a VPC connector that bridges Cloud Run and your VPC.

### What It Does

- Creates `redis-connector` in `us-central1`
- Uses IP range `10.8.0.0/28` (separate from Redis network)
- Min 2 instances, max 3 instances (e2-micro)
- Enables Cloud Run to reach `10.128.0.3` (Redis internal IP)

### Cost

Free tier covers 2 e2-micro instances = **$0/month** ✅

### Destroy

```powershell
.\destroy-vpc-connector.ps1
```

⚠️ Cloud Run services will lose VPC access!

## Usage in Services

When deploying to Cloud Run:

```powershell
gcloud run deploy service-name \
  --vpc-connector=redis-connector \
  --vpc-egress=private-ranges-only \
  --set-env-vars="ENVIRONMENT=production"
```

This allows the service to use internal IP `10.128.0.3` for Redis.

