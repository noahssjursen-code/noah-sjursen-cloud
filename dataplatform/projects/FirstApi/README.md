# FirstApi

**Live:** https://firstapi-766963653213.us-central1.run.app

FastAPI service deployed to GCP Cloud Run demonstrating:
- ✅ Cloud Run source-based deployment (no Docker!)
- ✅ Shared reusables library pattern (like C# class libraries)
- ✅ Redis integration with environment-based configuration
- ✅ VPC connector for internal Redis access
- ✅ Production-ready utilities (caching, counters, invalidation)

## Features

### Shared Library Pattern
Imports from organized `reusables/` structure:
- `reusables.redis` - Redis client and utilities
- `reusables.common` - General helpers

### Redis Integration
- **Local development**: Connects to external IP (34.66.188.104)
- **Production**: Connects via VPC to internal IP (10.128.0.3)
- Auto JSON serialization, TTL management, pattern matching

## Local Development

```powershell
# Install dependencies
pip install -r requirements.txt

# Run locally (connects to GCP Redis via public IP)
python main.py
```

Visit http://localhost:8080/docs for interactive API documentation.

## Endpoints

### Core
- `GET /` - Root endpoint with greeting from reusables library
- `GET /info` - API and library information
- `GET /health` - Health check
- `GET /docs` - Auto-generated interactive API docs

### Redis Operations
- `GET /redis/test` - Test Redis connection and show stats
- `POST /redis/set/{key}?value={value}` - Set a value (namespaced as `firstapi:data:{key}`)
- `GET /redis/get/{key}` - Get a value

### Examples

```powershell
# Test Redis connection
Invoke-WebRequest "https://firstapi-766963653213.us-central1.run.app/redis/test"

# Set a value
Invoke-WebRequest -Method POST "https://firstapi-766963653213.us-central1.run.app/redis/set/username?value=noah"

# Get a value
Invoke-WebRequest "https://firstapi-766963653213.us-central1.run.app/redis/get/username"
```

## Deploy to Production

Requires VPC connector for Redis access:

```powershell
# One-time setup: Create VPC connector
cd ../../iac/networking
.\setup-vpc-connector.ps1

# Deploy FirstApi
cd ../../projects/FirstApi
.\deploy.ps1
```

Deployment script:
- Copies `reusables/` into deployment package
- Sets `ENVIRONMENT=production` (uses internal Redis IP)
- Configures VPC connector for internal network access
- Cleans up temporary files

## Architecture

```
FirstApi (Cloud Run)
    ↓ VPC Connector
    ↓
Redis Server (10.128.0.3)
    - e2-micro (free tier)
    - 768MB memory
    - Protected mode off
    - Persistent storage
```

### Key Namespacing

All keys are automatically namespaced to prevent collisions:
- Pattern: `firstapi:data:{key}`
- Example: `POST /redis/set/user` → `firstapi:data:user`

This allows multiple services to share the same Redis instance safely.

## Reusables Library

Imports from organized structure:

```python
from reusables.common import get_greeting, get_library_info
from reusables.redis import (
    get_redis_client,    # Core client
    cache_set, cache_get,  # Cache helpers
    make_key,            # Key namespacing
    set_value, get_value,  # CRUD operations
    purge_cache,         # Invalidation
    increment, decrement,  # Counters
)
```

Full Redis library includes:
- CRUD operations with JSON serialization
- Bulk operations (set/get/delete many)
- Pattern matching and cache invalidation
- Counter operations
- Hash operations for structured data
- TTL management

## Environment Variables

- `ENVIRONMENT` - `local` or `production` (auto-set by deploy script)
- `REDIS_HOST` - Override default Redis host
- `REDIS_PORT` - Override default Redis port (6379)
- `PORT` - Server port (Cloud Run sets this to 8080)

## Technologies

- **Framework**: FastAPI 0.115+
- **Server**: Uvicorn
- **Cache**: Redis 7.0.15
- **Cloud**: GCP Cloud Run
- **Language**: Python 3.11+

