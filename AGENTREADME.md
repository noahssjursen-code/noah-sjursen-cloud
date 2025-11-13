# Agent Instructions

## Project Pattern

Each folder defining a module or service contains an `AGENTREADTHIS.md` file with instructions on what happens in that folder.

## Current Structure

- `dataplatform/iac/` - Infrastructure automation scripts
  - `gcloud-commands/` - Reusable gcloud CLI commands
- `dataplatform/projects/` - Applications and libraries
  - `reusables/` - Shared libraries
  - Individual project folders (each with AGENTREADTHIS.md)

## Technology-Specific Guidelines

Read these before working on specific types of projects:

- `dataplatform/projects/AGENTREADTHIS-SVELTEKIT.md` - SvelteKit app patterns
- `dataplatform/projects/AGENTREADTHIS-FASTAPI.md` - FastAPI backend patterns
- `dataplatform/projects/AGENTREADTHIS-CLOUDRUN.md` - Cloud Run deployment patterns
- `dataplatform/projects/reusables/python/AGENTREADTHIS.md` - Python library creation blueprint

## Navigation

Always read the `AGENTREADTHIS.md` in each folder before making changes.

