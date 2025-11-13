# Noah Sjursen Cloud

Personal cloud platform for production-grade projects and infrastructure experimentation.

## About

This repository houses my personal cloud infrastructure on Google Cloud Platform. It's structured like a professional data platform with reusable libraries and infrastructure as code, providing a foundation for future production-grade projects.

## Projects

### 🎛️ Cloud Control Center
GCP management dashboard for executing commands, monitoring resources, and controlling cloud infrastructure from a single interface. Built with FastAPI + SvelteKit.

**Status:** 🚧 In development

### 📚 Reusables Library
Shared Python libraries (Redis client, Gemini AI wrapper, common utilities) used across all projects.

## Infrastructure

### Current Resources

Clean slate - no active cloud resources. Infrastructure is created on-demand using automated scripts.

### Infrastructure as Code

All infrastructure managed via PowerShell + `gcloud` CLI:
- `iac/redis/` - Redis server setup/teardown scripts
- `iac/networking/` - VPC connector configuration scripts
- `iac/gcloud-commands/` - Reusable gcloud commands library

**Philosophy:** Simple, reproducible, portable. No Terraform complexity.

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
│   ├── iac/                           # Infrastructure automation
│   │   ├── cloud-control-center/      # OAuth & SA setup
│   │   └── gcloud-commands/           # Reusable gcloud commands
│   └── projects/
│       ├── cloud-control-center/      # GCP management dashboard
│       │   ├── api/                   # FastAPI backend
│       │   └── dashboard/             # SvelteKit frontend
│       └── reusables/                 # Shared libraries
│           └── python/                # Python utilities
│               ├── redis/             # Redis client
│               ├── gemini/            # AI client
│               ├── gcp/               # GCP IAM utilities
│               └── common/            # Common utilities
├── AGENTREADME.md                     # AI agent instructions
└── README.md                          # This file
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

**`reusables.python.gcp`**
- IAM permission checking
- Project access validation
- User role retrieval

**Design Goal:** Write once, use everywhere. Easy to extract for open-source.

## Quick Start

### Run Cloud Control Center

**First time:**
```powershell
cd dataplatform/projects/cloud-control-center
.\startNbuild.ps1
```

**After that:**
```powershell
.\start.ps1
```

Opens at `http://localhost:8080`

### Setup Infrastructure (when needed)

Infrastructure scripts available in `iac/` - run on-demand to create Redis, VPC connectors, or other cloud resources.

## Development Philosophy

- **Practical over perfect** - Ship working solutions
- **Cost-conscious** - Free tier where possible
- **Reusable code** - Build once, extract for OSS if useful
- **Self-hosting first** - Own your data, deploy anywhere
- **No enterprise bloat** - Keep it simple and fast

## What's Next

- Complete Cloud Control Center (command execution, resource monitoring, Google auth)
- Logging/monitoring service integrated with the control center
- Production microservices leveraging the reusables foundation
- Portable deployment system (one command to new GCP projects)

## Connect

- **GitHub:** [noahssjursen-code](https://github.com/noahssjursen-code)
- **Email:** noah.s.sjursen@gmail.com

---

## For AI Agents

This project uses structured agent instructions for better AI collaboration:

- **Start here:** [`AGENTREADME.md`](AGENTREADME.md) - Navigation and project patterns
- **Folder-specific:** Each module/service has an `AGENTREADTHIS.md` with detailed guidance
- **Technology guides:** See `dataplatform/projects/AGENTREADTHIS-*.md` for SvelteKit, FastAPI, and Cloud Run patterns

Read the appropriate documentation before making changes.

---

**Built with:** Python • FastAPI • SvelteKit • GCP • Gemini AI • PowerShell

*Learning in public. Building infrastructure. One project at a time.* 🚀
