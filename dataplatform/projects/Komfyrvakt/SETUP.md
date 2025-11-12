# Komfyrvakt Setup Guide

## Prerequisites

- Python 3.11+
- Node.js 20+
- Redis (or use provided Docker setup)

## Quick Setup

### 1. Get Gemini API Key (Free)

Visit https://aistudio.google.com/apikey and create a free API key.

### 2. Configure Environment

Create `.env` file in Komfyrvakt root:

```bash
# Copy example
cp .env.example .env

# Edit .env and add your Gemini key:
GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Start Komfyrvakt

```powershell
.\start.ps1
```

On first run:
- API dependencies install automatically
- Dashboard builds automatically
- API key auto-generates and displays

**Copy the API key from terminal output!**

### 4. Open Dashboard

Visit `http://localhost:8080`

Enter the API key you copied.

Done! 🔥

---

## Configuration Options

All settings in `.env`:

```bash
# Auto-generated on first run
KOMFYRVAKT_API_KEY=

# Redis (default: localhost for local dev)
REDIS_HOST=localhost
REDIS_PORT=6379

# For production, point to your Redis server:
# REDIS_HOST=10.128.0.3  # GCP internal IP

# Log retention
LOG_RETENTION_HOURS=48

# AI (Required for analysis features)
GEMINI_API_KEY=your_key_here
```

---

## Docker Deployment

### With Docker Compose:

```bash
# Set your Gemini key as environment variable
export GEMINI_API_KEY=your_actual_key_here

# Start everything
docker-compose up
```

Or use `.env` file in Komfyrvakt root:
```bash
# .env
GEMINI_API_KEY=your_actual_key_here

# Then just run:
docker-compose up
```

Services:
- API + Dashboard: `http://localhost:8080`
- Redis: Internal

---

## GCP Cloud Run Deployment

Coming soon - will handle environment variables automatically:

```powershell
cd gcp_deployment
.\deploy.ps1 -GeminiApiKey "your_key"
```

---

## Troubleshooting

**"AI analysis not configured"**
- Make sure `GEMINI_API_KEY` is set in `.env`
- Get free key: https://aistudio.google.com/apikey

**"Failed to connect to Redis"**
- For local: Ensure Redis is running (`docker run -d -p 6379:6379 redis`)
- For GCP: Check VPC connector and internal IP

**Dashboard not loading**
- Run `.\build-dashboard.ps1` to rebuild
- Check `dashboard/build/` folder exists

**API key not persisting**
- Check `.env` file exists in Komfyrvakt root
- API auto-generates and saves on first run

---

## Development

**API only:**
```powershell
cd api
python main.py
```

**Dashboard only (dev mode with hot reload):**
```powershell
cd dashboard
npm run dev
# Opens on http://localhost:3000
```

**Build dashboard for production:**
```powershell
.\build-dashboard.ps1
```

