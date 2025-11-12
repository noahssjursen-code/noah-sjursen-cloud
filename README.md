# Noah Sjursen Cloud

Personal cloud platform for production-grade projects and infrastructure experimentation.

## About

This repository houses my personal cloud infrastructure and projects on Google Cloud Platform. It's structured like a professional data platform with reusable libraries, infrastructure as code, and multiple deployed services.

## Projects

### 🔥 Komfyrvakt
**Self-hostable logging service with AI analytics** | [Docs](dataplatform/projects/Komfyrvakt)

- FastAPI backend + SvelteKit dashboard
- Redis hot storage with smart caching
- AI-powered log analysis (Gemini)
- Time series trend detection
- Group-based organization
- One-command deployment

**Status:** ✅ Production-ready | Self-hostable | GCP deployable

### 🚀 FirstApi
**Demo API with shared libraries** | [Live](https://firstapi-766963653213.us-central1.run.app) | [Docs](https://firstapi-766963653213.us-central1.run.app/docs)

- Cloud Run deployment demonstration
- Shared reusables integration
- Redis connectivity example

**Status:** ✅ Live on GCP Cloud Run

## Infrastructure

### Current Resources

- **Redis Server**: e2-micro Compute Engine instance (shared across projects)
  - External IP: `34.66.188.104` (development)
  - Internal IP: `10.128.0.3` (production via VPC)
  - 768MB RAM with LRU eviction
  - Free tier eligible

- **VPC Connector**: `vpc-connector-us-central1`
  - Enables Cloud Run → Compute Engine connectivity
  - Private network access for services

### Infrastructure as Code

All infrastructure managed via PowerShell + `gcloud` CLI:
- `iac/redis/` - Redis server setup/teardown
- `iac/networking/` - VPC connector configuration

**Philosophy:** Simple, reproducible, no Terraform complexity.

## Tech Stack

**Languages:**
- Python (primary for personal projects)
- TypeScript/JavaScript (frontend)
- PowerShell (infrastructure automation)
- Go (planned for performance-critical reusables)

**Cloud & Infrastructure:**
- Google Cloud Platform (Cloud Run, Compute Engine, VPC)
- Redis (caching, hot storage)
- Docker (containerization)

**Frameworks:**
- FastAPI (Python APIs)
- SvelteKit (frontend dashboards)
- TailwindCSS (styling)

**AI/ML:**
- Google Gemini (log analysis, insights)
- Structured JSON output for parsing

## Repository Structure

```
noah-sjursen-cloud/
├── dataplatform/
│   ├── iac/                    # Infrastructure automation
│   │   ├── redis/              # Redis server scripts
│   │   └── networking/         # VPC connector setup
│   └── projects/
│       ├── reusables/          # Shared libraries
│       │   ├── python/         # Python utilities
│       │   │   ├── redis/      # Redis client
│       │   │   └── gemini/     # AI client
│       │   └── go/             # Go utilities (planned)
│       ├── Komfyrvakt/         # Logging service
│       └── FirstApi/           # Demo API
└── README.md                   # This file
```

## Reusables Library

Cross-project utilities designed for reuse:

**`reusables.python.redis`**
- Singleton Redis client with auto-configuration
- Namespaced key helpers
- CRUD, bulk ops, pattern matching
- Cache helpers with TTL
- Counter operations, hash operations

**`reusables.python.gemini`**
- Gemini AI client wrapper
- Text generation with streaming
- JSON output parsing
- Code block stripping utilities

**Design Goal:** Write once, use everywhere. Easy to extract for open-source.

## Quick Start

### Run Komfyrvakt Locally

```powershell
cd dataplatform/projects/Komfyrvakt
.\start.ps1
```

Automatically:
1. Installs dependencies
2. Builds dashboard
3. Starts server on port 8080

### Deploy to GCP

```powershell
cd dataplatform/projects/FirstApi
.\deploy.ps1
```

Uses Cloud Build to deploy with buildpacks (no manual Docker).

## Development Philosophy

- **Practical over perfect** - Ship working solutions
- **Cost-conscious** - Free tier where possible
- **Reusable code** - Build once, extract for OSS if useful
- **Self-hosting first** - Own your data, deploy anywhere
- **No enterprise bloat** - Keep it simple and fast

## Future Projects

- AI-powered video generation pipeline
- Asset tracking system (Obsero rebuild)
- More microservices with shared Redis
- SDK clients (Python, JavaScript, Go)

## Connect

- **GitHub:** [noahssjursen-code](https://github.com/noahssjursen-code)
- **Email:** noah.s.sjursen@gmail.com

---

**Built with:** Python • FastAPI • SvelteKit • Redis • GCP • Gemini AI

*Learning in public. Building useful tools. Sharing the journey.* 🚀
