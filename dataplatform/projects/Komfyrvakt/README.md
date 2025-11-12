# Komfyrvakt 🔥

**Self-hostable logging service with AI-powered analytics and time series visualization.**

> *Komfyrvakt (Norwegian: "stove guard") - The device that prevents kitchen fires. Similarly, Komfyrvakt watches your systems 24/7, preventing infrastructure fires before they happen.*

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115+-green.svg)](https://fastapi.tiangolo.com/)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-2.0-orange.svg)](https://kit.svelte.dev/)
[![Redis](https://img.shields.io/badge/Redis-7.0-red.svg)](https://redis.io/)

---

## What It Does

Send logs from apps, IoT devices, or services. Query them fast. Get AI insights. Visualize trends.

**No complex setup. No multi-tenant overhead. Just logging that works.**

```bash
# Post a log
curl -X POST http://localhost:8080/api/logs \
  -H "Authorization: Bearer kmf_your_key" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Temperature reading",
    "level": "warning",
    "group": "datacenter:server-rack-1",
    "tags": ["temperature", "monitoring"],
    "data": {"temperature": 8.5, "threshold": 6.0}
  }'

# Query logs
curl http://localhost:8080/api/logs?group=datacenter:* \
  -H "Authorization: Bearer kmf_your_key"

# View dashboard
open http://localhost:8080
```

---

## Key Features

- ⚡ **Fast Queries** - Redis-backed with indexed groups and tags
- 🤖 **AI Analysis** - Gemini-powered insights with structured findings and recommendations
- 📈 **Time Series** - Automatic trend detection and visualization
- 🗂️ **Smart Organization** - Hierarchical groups with prefix matching
- 📊 **Live Dashboard** - Full-screen panel layout, iframe-embeddable
- 💾 **Smart Caching** - AI reports cached 2hr, time series 30min
- 🐳 **Self-Hostable** - Docker Compose or bare metal
- ☁️ **Cloud Ready** - Deploy to GCP Cloud Run, AWS, Azure
- 🔐 **API Key Auth** - Auto-generated on first run
- 💰 **Cost Effective** - Optimized for free tier usage

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│              Your Applications                  │
│   (APIs, IoT devices, microservices, etc.)     │
└────────────────┬────────────────────────────────┘
                 │ POST /api/logs
                 ↓
┌─────────────────────────────────────────────────┐
│        Komfyrvakt (Single Server:8080)          │
│  ┌──────────────┬───────────────────────────┐   │
│  │ API Routes   │  Dashboard (SvelteKit)    │   │
│  │ (/api/*)     │  (/)                      │   │
│  │              │                           │   │
│  │ • Ingest     │  • Real-time viewer       │   │
│  │ • Query      │  • AI insights panel      │   │
│  │ • Analyze    │  • Time series charts     │   │
│  │ • Purge      │  • Group navigation       │   │
│  └──────┬───────┴───────────────────────────┘   │
│         ↓                                        │
│  ┌─────────────────┐                            │
│  │  Redis (Hot)    │                            │
│  │  48hr retention │                            │
│  └─────────────────┘                            │
└─────────────────────────────────────────────────┘
```

**Data Organization:**
- **Groups**: Hierarchical namespacing (`datacenter:server-rack-1`, `app:api:prod`)
- **Tags**: Flexible filtering (`temperature`, `alert`, `performance`)
- **Time Series**: Auto-generated 5-minute interval aggregations

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11+, FastAPI, Pydantic |
| Frontend | SvelteKit, TypeScript, TailwindCSS, Chart.js |
| Storage | Redis 7.0 (hot), Optional GCS/Firestore (cold) |
| AI | Google Gemini 2.0 Flash Lite |
| Deployment | Docker, Cloud Run, Compute Engine |
| Shared Libs | `reusables.python` (redis, gemini) |

---

## Quick Start

### One-Command Startup

```powershell
.\start.ps1
```

**Automatically:**
1. Installs Python dependencies
2. Builds SvelteKit dashboard
3. Starts server on `http://localhost:8080`
4. Prompts for Gemini API key (optional, for AI features)

**First run:** API key auto-generated and displayed in terminal.

### With Docker Compose

```bash
# Clone repo
git clone https://github.com/noahssjursen-code/noah-sjursen-cloud.git
cd noah-sjursen-cloud/dataplatform/projects/Komfyrvakt

# Add your Gemini key (optional)
echo "GEMINI_API_KEY=your_key_here" >> .env

# Start everything
docker-compose up
```

**Services:**
- Dashboard + API: `http://localhost:8080`
- Redis: Internal (port 6379)

---

## Configuration

Create `.env` file in Komfyrvakt root:

```bash
# Auto-generated on first run
KOMFYRVAKT_API_KEY=kmf_generated_key

# Redis connection
REDIS_HOST=localhost  # or your Redis server IP
REDIS_PORT=6379

# AI features (optional)
# Get free key: https://aistudio.google.com/apikey
GEMINI_API_KEY=your_gemini_api_key

# Storage
LOG_RETENTION_HOURS=48
ENVIRONMENT=local
```

See [SETUP.md](SETUP.md) for detailed configuration options.

---

## API Reference

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/logs` | Ingest single log |
| POST | `/api/logs/batch` | Ingest multiple logs |
| GET | `/api/logs` | Query logs with filters |
| GET | `/api/logs/{id}` | Get specific log |
| GET | `/api/groups` | List all groups |
| POST | `/api/analyze` | AI analysis with time series |
| DELETE | `/api/purge` | Purge logs by group |
| GET | `/api/stats` | Platform statistics |
| GET | `/api/health` | Health check |

**Authentication:** All endpoints require `Authorization: Bearer kmf_your_key`

**Full API docs:** `http://localhost:8080/api/docs` (interactive Swagger UI)

**Detailed documentation:** [DOCS.md](DOCS.md)

---

## AI Analysis Features

### Structured Insights

AI returns JSON with:
- **Summary**: System health overview
- **Severity**: `normal` | `warning` | `critical`
- **Findings**: Issues with temporal context
- **Recommendations**: Prioritized actions (high/medium/low)

### Time Series Analysis

- Auto-generates 5-minute interval aggregations
- Tracks all numeric fields (temperature, CPU, latency, etc.)
- Detects trends (rising, falling, spikes)
- Cached separately for performance

### Example Response

```json
{
  "summary": "System showing elevated CPU with temperature spike at 10:30 PM",
  "severity": "warning",
  "findings": [
    {
      "title": "CPU Usage Spike",
      "description": "CPU jumped from 45% to 78% over 15 minutes",
      "severity": "warning"
    }
  ],
  "recommendations": [
    {
      "action": "Investigate process causing CPU spike",
      "priority": "high"
    }
  ]
}
```

---

## Dashboard

**Full-screen panel layout** optimized for monitoring and iframe embedding:

- **Left Sidebar**: Group navigation
- **Center (70%)**: AI insights, metrics, time series charts
- **Right Sidebar (30%)**: Recent logs (compact view)

**Features:**
- ✅ Auto-loading API key
- ✅ Expandable time series charts (Chart.js)
- ✅ Real-time log streaming
- ✅ Search and filter
- ✅ Color-coded severity levels
- ✅ Collapsible data fields
- ✅ Responsive design

---

## Use Cases

**IoT Monitoring:**
```json
{
  "group": "warehouse:freezer-3",
  "data": {"temperature": -18.5, "humidity": 45}
}
```

**API Logging:**
```json
{
  "group": "service:api:prod",
  "data": {"duration_ms": 234, "status": 200}
}
```

**Infrastructure:**
```json
{
  "group": "datacenter:server-rack-1",
  "data": {"cpu": 67, "memory": 82, "disk_io": 450}
}
```

**Application Events:**
```json
{
  "group": "app:obsero:prod",
  "tags": ["user-action", "critical"],
  "data": {"user_id": "123", "action": "delete_asset"}
}
```

---

## Client Examples

### Python

```python
import requests

API_KEY = "kmf_your_api_key"
BASE_URL = "http://localhost:8080/api"

# Post log
requests.post(
    f"{BASE_URL}/logs",
    headers={"Authorization": f"Bearer {API_KEY}"},
    json={
        "message": "User logged in",
        "level": "info",
        "group": "app:auth",
        "tags": ["authentication"],
        "data": {"user_id": "noah@example.com"}
    }
)

# Query logs
logs = requests.get(
    f"{BASE_URL}/logs?group=app:*&limit=50",
    headers={"Authorization": f"Bearer {API_KEY}"}
).json()
```

### JavaScript/TypeScript

```typescript
const API_KEY = 'kmf_your_api_key';
const BASE_URL = 'http://localhost:8080/api';

// Post log
await fetch(`${BASE_URL}/logs`, {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    message: 'Payment processed',
    level: 'info',
    group: 'payments:stripe',
    tags: ['transaction', 'success'],
    data: { amount: 99.99, currency: 'USD' }
  })
});
```

### PowerShell

```powershell
$apiKey = "kmf_your_api_key"
$headers = @{"Authorization" = "Bearer $apiKey"}

# Post log
Invoke-RestMethod -Uri "http://localhost:8080/api/logs" `
  -Method POST -Headers $headers -Body (@{
    message = "Backup completed"
    level = "info"
    group = "backup:database"
    data = @{ duration_min = 45; size_gb = 120 }
  } | ConvertTo-Json)
```

---

## Deployment

### Self-Hosting (Recommended)

**Docker Compose:**
```bash
docker-compose up -d
```

**Bare Metal:**
```powershell
.\start.ps1
```

### GCP Cloud Run

Coming soon - automated deployment script.

---

## Project Status

**✅ Production Features:**
- Log ingestion (single + batch)
- Fast querying with filters
- Group-based organization
- API key authentication
- Redis hot storage
- SvelteKit dashboard
- AI analysis with Gemini
- Time series aggregation
- Smart caching (2hr AI, 30min time series)
- Full-screen panel layout
- Chart.js visualization

**🚧 Planned:**
- CI/CD pipeline (GitHub Actions)
- Unit tests (pytest, vitest)
- GCP deployment automation
- Cold storage integration
- SDK clients (Python, JS, Go)
- WebSocket live streaming
- Export to CSV/JSON
- Dark mode

**📊 Current Stats:**
- Built in: ~4 hours
- Lines of code: ~2,500+
- API endpoints: 10
- Cache strategies: 2 (analysis, time series)
- Deployment options: 3 (local, Docker, Cloud Run)

---

## Documentation

- [SETUP.md](SETUP.md) - Detailed setup instructions
- [DOCS.md](DOCS.md) - Complete API reference
- [CURRENT.md](CURRENT.md) - Development progress tracker

---

## Why Komfyrvakt?

**vs ELK Stack:** Simpler setup, AI-powered, lighter footprint  
**vs CloudWatch:** Self-hostable, customizable, no vendor lock-in  
**vs Datadog:** Free, open source, own your data  
**vs Splunk:** No complexity, modern UI, AI built-in

**Built for developers who want:**
- Logging without enterprise overhead
- Self-hosting control
- AI insights without manual analysis
- Fast queries without complex queries
- Beautiful dashboards without config hell

---

## Contributing

This is a personal learning project, but contributions welcome!

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Open a PR

**Coding style:** Practical > perfect. Ship it, then refine.

---

## License

MIT License - use it, fork it, self-host it, do whatever you want with it.

---

## Acknowledgments

Built as part of [noah-sjursen-cloud](https://github.com/noahssjursen-code/noah-sjursen-cloud) - my personal cloud platform for learning GCP, DevOps, and full-stack development.

**Inspired by:**
- My professional work with Azure + Redis
- Need for simple, self-hostable logging
- Previous project: WatchTower (multi-tenant version, deprecated)

---

**Komfyrvakt** - *Simple logging. Fast queries. AI insights. Zero fires.* 🔥

**Built by [Noah Sjursen](https://github.com/noahssjursen-code)** | 21 | Software Developer | Norway 🇳🇴
