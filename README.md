# Noah Sjursen Cloud

Personal cloud platform and portfolio demonstrating authentication systems, infrastructure automation, and cloud service integration.

**Portfolio Notice:** This repository is a personal learning and demonstration project. It is not intended for production use, cloning, or deployment by others. All code and infrastructure patterns are specific to my personal GCP environment and workflow.

## About

This repository showcases my personal cloud infrastructure on Google Cloud Platform. It demonstrates OAuth 2.0 authentication, role-based access control with custom IAM roles, infrastructure automation via PowerShell, and reusable service architectures.

## Projects

### Cloud Control Center
GCP management dashboard with OAuth 2.0 authentication, role-based access control (RBAC), and resource monitoring. Implements custom IAM roles, user management, and real-time GCP resource tracking.

**Status:** Core features complete - User Management, RBAC, OAuth 2.0

**Features:**
- Google OAuth 2.0 authentication
- Custom IAM roles (Viewer, Operator, Admin)
- User management (admin-only)
- Resource monitoring (Compute, Cloud Run, Storage)
- Dark/light mode UI
- Role-based access control

### Reusables Library
Shared Python libraries used across all projects. Demonstrates clean abstraction patterns and reusable service architectures.

## Infrastructure

### Current Resources

Clean slate - no active cloud resources. Infrastructure is created on-demand using automated scripts.

### Infrastructure as Code

All infrastructure managed via PowerShell + `gcloud` CLI:
- `iac/cloud-control-center/` - OAuth setup, custom IAM roles, role assignment/revocation
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
- IAM permission checking and project access validation
- User role retrieval and level detection
- GCP resource listing (Compute, Cloud Run, Storage)
- User management (list, assign roles, revoke roles)
- Execute gcloud commands with JSON parsing
- Custom role assignment/revocation utilities

**Design Goal:** Write once, use everywhere. Demonstrates modular, reusable architecture patterns.

## Local Development

These instructions are for personal reference and demonstrate the deployment workflow.

### Cloud Control Center

**Initial Setup (one-time):**
```powershell
# Setup OAuth credentials
cd dataplatform/iac/cloud-control-center
.\bootstrap.ps1 <project-id> -OAuth

# Create custom IAM roles
.\bootstrap.ps1 <project-id> -CustomRoles

# Assign admin access
.\assign-role.ps1 <project-id> your-email@gmail.com admin
```

**Run Locally:**
```powershell
cd ../../projects/cloud-control-center

# First time or after code changes
.\startNbuild.ps1

# Subsequent runs
.\start.ps1
```

Opens at `http://localhost:8080`

### Infrastructure Management

Infrastructure scripts in `iac/` demonstrate automated provisioning patterns for Redis, VPC connectors, and custom IAM roles.

## Development Philosophy

- **Practical over perfect** - Ship working solutions
- **Cost-conscious** - Free tier where possible
- **Reusable patterns** - Build modular, maintainable systems
- **Security-first** - Implement proper authentication and authorization
- **Learn by building** - Real infrastructure, real problems, real solutions

## Roadmap

Planned features and enhancements to demonstrate additional cloud platform capabilities:

- Deploy Cloud Control Center to Cloud Run (production hosting)
- Add resource management actions (start/stop VMs, deploy services)
- Build logging/monitoring service integrated with control center
- Expand operator role capabilities (service deployments, scaling)
- Production microservices leveraging the reusables foundation
- Infrastructure cloning automation (demonstrating portable IaC patterns)

## Connect

- **GitHub:** [noahssjursen-code](https://github.com/noahssjursen-code)
- **Email:** noah.s.sjursen@gmail.com

---

## License & Usage

This repository is for portfolio and demonstration purposes only. All code is provided as-is without warranty. Not licensed for use, modification, or distribution by third parties. If you're interested in my work or would like to discuss collaboration, please reach out via the contact information above.

---

## For AI Agents

This project uses structured agent instructions for better AI collaboration:

- **Start here:** [`AGENTREADME.md`](AGENTREADME.md) - Navigation and project patterns
- **Folder-specific:** Each module/service has an `AGENTREADTHIS.md` with detailed guidance
- **Technology guides:** See `dataplatform/projects/AGENTREADTHIS-*.md` for SvelteKit, FastAPI, and Cloud Run patterns

Read the appropriate documentation before making changes.

---

**Built with:** Python • FastAPI • SvelteKit • GCP • Gemini AI • PowerShell

*Portfolio demonstration of cloud infrastructure, authentication systems, and modern development patterns.*
