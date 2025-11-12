# Komfyrvakt

**Simple, self-hostable logging service with AI analytics.**

> *Komfyrvakt (Norwegian: "stove guard") - Like the device that prevents your stove from burning down your house, Komfyrvakt watches your systems 24/7.*

## What It Does

Send logs from your apps, IoT devices, or services. Query them fast. Get AI-powered insights.

**No complex setup. No multi-tenant overhead. Just logging that works.**

### Example Use Case

You have temperature sensors in multiple fridges posting readings every 10 seconds:

```json
POST /logs
{
  "message": "Temperature reading",
  "level": "info",
  "tags": ["fridge-1", "building-a"],
  "data": {"temperature": 4.2, "humidity": 65},
  "timestamp": "2025-11-12T20:15:30Z"
}
```

Query them:
```
GET /logs?tags=fridge-1&level=warning&since=2025-11-12
```

Get AI insights:
```
GET /analytics/report?tags=fridge-1&days=7
```

Komfyrvakt handles storage, querying, graphing, and AI analysis.

## Features

- ⚡ **Fast** - Redis-backed hot storage for recent logs
- 🔍 **Flexible** - Tag-based filtering (no rigid schemas)
- 🤖 **AI Analytics** - Automated pattern detection and reports
- 📊 **Dashboard** - React-based real-time log viewer
- 🐳 **Self-hostable** - Docker Compose for easy deployment
- ☁️ **Cloud-ready** - Runs on GCP Cloud Run (or any cloud)
- 💰 **Cost-effective** - Optimized for free tier

## Architecture

```
Your Apps/Sensors
    ↓ POST /logs
Komfyrvakt API (FastAPI)
    ↓
Redis (hot logs, fast queries)
    ↓ (optional background job)
Firestore/BigQuery (cold storage)
    ↓
AI Service (Gemini/OpenAI)
    ↓
Dashboard (React)
```

**Tag-based organization:**
- No complex tenancy
- Filter by any combination of tags
- `tags: ["production", "api-gateway", "europe"]`

## Tech Stack

- **Backend**: Python + FastAPI
- **Cache**: Redis (recent logs, fast access)
- **Storage**: Firestore or BigQuery (long-term, optional)
- **AI**: Gemini / OpenAI
- **Frontend**: React + Vite + TypeScript  
- **Deployment**: Docker Compose or Cloud Run
- **Shared**: `reusables.python` library

## Quick Start

### Self-Hosted (Docker Compose)

```bash
git clone https://github.com/noahssjursen-code/noah-sjursen-cloud.git
cd noah-sjursen-cloud/dataplatform/projects/Komfyrvakt
docker-compose up
```

**Services start automatically:**
- API: `http://localhost:8080`
- Dashboard: `http://localhost:3000`
- Redis: `localhost:6379`

**On first run, an API key is auto-generated. Check API logs for the key.**

### Local Development (Without Docker)

**Option 1: Run both with script**
```powershell
.\start-local.ps1
```

**Option 2: Run separately**
```powershell
# Terminal 1 - API
cd api
pip install -r requirements.txt
python main.py

# Terminal 2 - Dashboard
cd dashboard
npm install
npm run dev
```

Visit `http://localhost:3000` and enter your API key!

### Cloud Deployment (GCP)

Coming soon - will deploy both API and dashboard to Cloud Run.

## API

**Authentication:** All endpoints require API key in header:
```
Authorization: Bearer kmf_your_api_key_here
```

### Send Logs

```bash
POST /logs
Headers:
  Authorization: Bearer kmf_your_api_key_here
  Content-Type: application/json

Body:
{
  "message": "Request completed",
  "level": "info",
  "tags": ["api", "production"],
  "data": {"duration_ms": 45, "status": 200},
  "timestamp": "2025-11-12T20:15:30Z"
}
```

### Query Logs

```bash
GET /logs?tags=api,production&level=error&since=2025-11-12&limit=100
Headers:
  Authorization: Bearer kmf_your_api_key_here
```

Returns recent logs matching filters.

### Get AI Insights

```bash
GET /analytics/report?tags=fridge-1&hours=24
```

Returns AI-generated summary, anomaly detection, and recommendations.

### Dashboard

Simple web UI for:
- Live log streaming
- Filter by tags, level, time
- Graphs and charts
- AI insights panel

## Log Structure

```json
{
  "id": "log_abc123",
  "message": "Temperature too high",
  "level": "warning",
  "tags": ["fridge-1", "building-a"],
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
├── dashboard/            # Frontend (SvelteKit) - Coming soon
│   └── README.md
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

🚧 **In Development** - Simple, self-hostable logging with AI analytics.

---

**Komfyrvakt** - *Simple logging. Fast queries. AI insights.* 🔥

