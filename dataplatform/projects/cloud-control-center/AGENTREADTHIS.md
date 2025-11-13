# Cloud Control Center

## What This Is

SvelteKit dashboard mounted with FastAPI for managing GCP resources.

## Structure

```
cloud-control-center/
├── api/                    # FastAPI backend
│   ├── main.py            # Main app, mounts dashboard
│   ├── routes/            # API endpoints
│   └── requirements.txt   # Python dependencies
└── dashboard/             # SvelteKit frontend
    ├── src/               # Svelte components
    └── build/             # Built static files (served by FastAPI)
```

## Features

- Google Cloud authentication
- Execute GCP commands from UI
- List running resources
- Command output display
- Future: integrate monitoring and other services

## Tech Stack

- **Backend:** FastAPI (Python)
- **Frontend:** SvelteKit (TypeScript)
- **Auth:** Google Cloud IAM
- **Deployment:** Cloud Run
- **Shared libs:** `reusables.python`

## Running Locally

```powershell
.\start.ps1
```

## Deployment

```powershell
.\deploy.ps1
```

