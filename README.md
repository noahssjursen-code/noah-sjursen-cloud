# Noah Sjursen Cloud

Personal cloud platform for production-grade projects and infrastructure experimentation.

## About

This repository houses my personal cloud infrastructure on Google Cloud Platform. It's structured like a professional data platform with reusable libraries and infrastructure as code, providing a foundation for future production-grade projects.

## Projects

Currently focused on building the reusable libraries foundation and infrastructure for future projects.

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
- Google Gemini (text generation, structured output)
- Reusable client wrapper for easy integration

## Repository Structure

```
noah-sjursen-cloud/
├── dataplatform/
│   ├── iac/                    # Infrastructure automation
│   │   ├── redis/              # Redis server scripts
│   │   └── networking/         # VPC connector setup
│   └── projects/
│       └── reusables/          # Shared libraries
│           ├── python/         # Python utilities
│           │   ├── redis/      # Redis client
│           │   ├── gemini/     # AI client
│           │   └── common/     # Common utilities
│           └── go/             # Go utilities (planned)
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

### Setup Infrastructure

```powershell
# Setup Redis server
cd dataplatform/iac/redis
.\setup-redis.ps1

# Setup VPC connector for Cloud Run services
cd ../networking
.\setup-vpc-connector.ps1
```

Infrastructure is managed via PowerShell scripts - simple, reproducible, no Terraform complexity.

## Development Philosophy

- **Practical over perfect** - Ship working solutions
- **Cost-conscious** - Free tier where possible
- **Reusable code** - Build once, extract for OSS if useful
- **Self-hosting first** - Own your data, deploy anywhere
- **No enterprise bloat** - Keep it simple and fast

## Future Projects

- Production-ready microservices built on the reusables foundation
- AI-powered data pipelines and analytics tools
- SDK clients (Python, JavaScript, Go) for common cloud operations
- Asset tracking and monitoring systems

## Connect

- **GitHub:** [noahssjursen-code](https://github.com/noahssjursen-code)
- **Email:** noah.s.sjursen@gmail.com

---

**Built with:** Python • Redis • GCP • Gemini AI • PowerShell

*Learning in public. Building the foundation. Preparing for scale.* 🚀
