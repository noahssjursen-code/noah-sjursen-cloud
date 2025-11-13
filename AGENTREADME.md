# Agent Instructions

## Project Pattern

Each folder defining a module or service contains an `AGENTREADTHIS.md` file with instructions on what happens in that folder.

## Current Structure

- `dataplatform/iac/` - Infrastructure automation scripts ([IaC Guide](dataplatform/iac/AGENTREADTHIS.md))
  - `gcloud-commands/` - Reusable gcloud CLI commands
  - Component folders with bootstrap.ps1 scripts
- `dataplatform/projects/` - Applications and libraries
  - `reusables/` - Shared libraries
  - Individual project folders (each with AGENTREADTHIS.md)

## Technology-Specific Guidelines

Read these before working on specific types of projects:

- `dataplatform/iac/AGENTREADTHIS.md` - Infrastructure as Code patterns and structure
- `dataplatform/projects/AGENTREADTHIS-SVELTEKIT.md` - SvelteKit app patterns
- `dataplatform/projects/AGENTREADTHIS-FASTAPI.md` - FastAPI backend patterns
- `dataplatform/projects/AGENTREADTHIS-CLOUDRUN.md` - Cloud Run deployment patterns
- `dataplatform/projects/reusables/python/AGENTREADTHIS.md` - Python library creation blueprint

## Navigation

Always read the `AGENTREADTHIS.md` in each folder before making changes.

