# Komfyrvakt

**Simple, self-hostable logging service with AI analytics.**

> *Komfyrvakt (Norwegian: "stove guard") - Like the device that prevents your stove from burning down your house, Komfyrvakt watches your systems 24/7.*

## What It Does

Send logs from your apps, IoT devices, or services. Query them fast. Get AI-powered insights.

**No complex setup. No multi-tenant overhead. Just logging that works.**

### Example Use Case

You have temperature sensors in multiple fridges posting readings every 10 seconds:

```json
POST /api/logs
{
  "message": "Temperature reading",
  "level": "info",
  "group": "restaurant-a:fridge-1",
  "tags": ["temperature", "monitoring"],
  "data": {"temperature": 4.2, "humidity": 65},
  "timestamp": "2025-11-12T20:15:30Z"
}
```

Query them:
```
GET /api/logs?group=restaurant-a:*&level=warning
```

View in dashboard:
```
http://localhost:8080
```

Komfyrvakt handles storage, querying, visualization, and AI analysis.

## Features

- ⚡ **Fast** - Redis-backed hot storage for recent logs
- 🗂️ **Group Organization** - Hierarchical grouping with prefix queries
- 🏷️ **Tag Filtering** - Flexible tag-based filtering
- 📊 **Dashboard** - SvelteKit real-time log viewer with auto-refresh
- 🤖 **AI Analytics** - Automated pattern detection (coming soon)
- 🐳 **Self-hostable** - Docker Compose for easy deployment
- ☁️ **Cloud-ready** - Runs on GCP Cloud Run (or any cloud)
- 💰 **Cost-effective** - Optimized for free tier
- 🔐 **Secure** - API key authentication

## Architecture

```
Your Apps/Sensors
    ↓ POST /api/logs
Komfyrvakt (Single Server - Port 8080)
    ├── API Routes (/api/*)
    │   └── Redis (log storage with TTL)
    └── Dashboard (/) - SvelteKit UI
```

**Organization:**
- **Groups** - Hierarchical (e.g., `restaurant-a:fridge-1`, `service:api:prod`)
- **Tags** - Flexible filtering (e.g., `["temperature", "alert", "critical"]`)
- Query by group prefix: `?group=restaurant-a:*`

## Tech Stack

- **Backend**: Python + FastAPI
- **Frontend**: SvelteKit + TypeScript + TailwindCSS
- **Cache**: Redis (48-hour retention with TTL)
- **Storage**: Optional cold storage (Firestore/BigQuery)
- **AI**: Gemini / OpenAI (coming soon)
- **Deployment**: Single server (Docker Compose or Cloud Run)
- **Shared**: `reusables.python` library

## Quick Start

**First time setup?** See [SETUP.md](SETUP.md) for detailed instructions.

### Self-Hosted (Docker Compose)

```bash
git clone https://github.com/noahssjursen-code/noah-sjursen-cloud.git
cd noah-sjursen-cloud/dataplatform/projects/Komfyrvakt
docker-compose up
```

**Services start automatically:**
- **Everything on one server:** `http://localhost:8080`
- Dashboard: `http://localhost:8080/`
- API: `http://localhost:8080/api/*`
- API Docs: `http://localhost:8080/api/docs`
- Redis: Internal

**On first run, an API key is auto-generated. Check terminal for the key.**

### Local Development (Without Docker)

**Quick Start (Automatic):**
```powershell
.\start.ps1
```

This will:
1. Install API dependencies
2. Build dashboard
3. Start the server

**Visit** `http://localhost:8080` - Dashboard loads, enter API key from terminal!

**Note:** AI features require `GEMINI_API_KEY` in `.env` file. Get free key at https://aistudio.google.com/apikey

**Manual (Step-by-step):**
```powershell
# 1. Build dashboard
.\build-dashboard.ps1

# 2. Install API deps
cd api
pip install -r requirements.txt

# 3. Run server
python main.py
```

### Cloud Deployment (GCP)

Coming soon - will deploy both API and dashboard to Cloud Run.

## API

**Authentication:** All endpoints require API key in header:
```
Authorization: Bearer kmf_your_api_key_here
```

### Send Logs

```bash
POST /api/logs
Headers:
  Authorization: Bearer kmf_your_api_key_here
  Content-Type: application/json

Body:
{
  "message": "Request completed",
  "level": "info",
  "group": "service:api:prod",
  "tags": ["performance"],
  "data": {"duration_ms": 45, "status": 200}
}
```

### Query Logs

```bash
GET /api/logs?group=service:api:*&level=error&limit=100
Headers:
  Authorization: Bearer kmf_your_api_key_here
```

**Filters:** `group`, `tags`, `level`, `since`, `until`, `source`, `limit`

### Dashboard

Visit `http://localhost:8080` for web UI:
- ✅ Real-time log viewer (auto-refresh every 5s)
- ✅ Filter by group, tags, level
- ✅ Color-coded log levels
- ✅ Expandable data fields
- ✅ Responsive design

**See [DOCS.md](DOCS.md) for complete API reference.**

## Log Structure

```json
{
  "id": "log_20251112201530_abc123",
  "message": "Temperature too high",
  "level": "warning",
  "group": "restaurant-a:fridge-1",
  "tags": ["temperature", "alert"],
  "data": {
    "temperature": 8.5,
    "threshold": 6.0
  },
  "timestamp": "2025-11-12T20:15:30Z",
  "source": "sensor-temp-001"
}
```

**Levels:** `debug`, `info`, `warning`, `error`, `critical`

## Project Structure

```
Komfyrvakt/
├── api/                  # Backend (Python/FastAPI)
│   ├── main.py           # API server
│   ├── models/           # Data models
│   ├── services/         # Business logic
│   ├── config/           # Configuration
│   ├── utils/            # Helpers
│   ├── requirements.txt
│   └── Dockerfile
├── dashboard/            # Frontend (SvelteKit + TypeScript + Tailwind)
│   ├── src/             # Svelte components and routes
│   └── build/           # Built static files (served by API)
├── docker-compose.yml    # Self-hosting (runs both)
├── README.md             # This file
├── DOCS.md               # API documentation
└── CURRENT.md            # Development status
```

## Why Komfyrvakt?

**vs ELK Stack:** Simpler, lighter, AI-powered  
**vs CloudWatch:** Self-hostable, cheaper, customizable  
**vs Datadog:** Free, open source, own your data  

Built for developers who want logging without the enterprise overhead.

## Status

✅ **Core Functionality Working** - Log ingestion, querying, dashboard live!

🚧 **In Progress** - AI analytics, cold storage, Docker deployment

---

**Komfyrvakt** - *Simple logging. Fast queries. AI insights.* 🔥

