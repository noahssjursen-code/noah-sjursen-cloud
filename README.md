# Noah Sjursen Cloud

Personal cloud platform for learning and experimentation.

## Projects

**FirstApi** - [Live](https://firstapi-766963653213.us-central1.run.app) | [Docs](https://firstapi-766963653213.us-central1.run.app/docs)

Simple FastAPI service deployed to GCP Cloud Run. Demonstrates shared library pattern across services.

## Tech

- Python + FastAPI
- Google Cloud Run
- Redis (shared server)

## Structure

```
dataplatform/
├── iac/
│   ├── redis/         # Redis server (e2-micro, free tier)
│   └── networking/    # VPC connectors
└── projects/
    ├── reusables/     # Shared utilities (Redis client, etc.)
    └── FirstApi/      # Deployed API with Redis integration
```

## Run Locally

```bash
cd dataplatform/projects/FirstApi
pip install -r requirements.txt
python main.py
```
