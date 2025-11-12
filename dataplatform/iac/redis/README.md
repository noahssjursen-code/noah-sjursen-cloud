# Redis Infrastructure

Scripts to manage shared Redis server on GCP (free tier e2-micro).

## Setup

```powershell
.\setup-redis.ps1
```

Creates a Redis server and outputs the internal IP to use in your services.

## Destroy

```powershell
.\destroy-redis.ps1
```

⚠️ Deletes the Redis server and all data.

## What You Get

- Free tier e2-micro instance (768MB Redis)
- Internal VPC access only (secure)
- Persistent storage (survives restarts)
- Shareable across all Cloud Run services

## Connect from Services

Use the internal IP from setup:

```python
import redis
r = redis.Redis(host='10.128.0.X', port=6379)
```

