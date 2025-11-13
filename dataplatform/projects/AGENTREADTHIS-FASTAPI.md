# FastAPI Apps - Standard Pattern

## Project Structure

```
project-name/
├── api/
│   ├── main.py               # FastAPI app entry point
│   ├── routes/               # Route modules (optional)
│   │   ├── __init__.py
│   │   └── commands.py
│   ├── models/               # Pydantic models (optional)
│   │   ├── __init__.py
│   │   └── request.py
│   ├── services/             # Business logic (optional)
│   │   ├── __init__.py
│   │   └── gcp_service.py
│   └── requirements.txt      # Python dependencies
└── dashboard/                 # SvelteKit frontend
```

## Main App Setup

```python
import sys
import os

# Add reusables to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI(
    title="App Name",
    description="Description",
    version="0.1.0",
    docs_url="/api/docs"
)

# API routes
@app.get("/api")
def root():
    return {"service": "Name", "version": "0.1.0"}

@app.get("/api/health")
def health():
    return {"status": "healthy"}

# Mount dashboard LAST
dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'build')
if os.path.exists(dashboard_path):
    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

## Route Organization

For larger apps, split routes into modules:

```python
# api/routes/commands.py
from fastapi import APIRouter

router = APIRouter(prefix="/api/commands", tags=["commands"])

@router.get("/list")
def list_commands():
    return {"commands": []}

# api/main.py
from routes.commands import router as commands_router
app.include_router(commands_router)
```

## Pydantic Models

```python
from pydantic import BaseModel, Field
from typing import Optional

class RequestModel(BaseModel):
    name: str = Field(..., description="Name field")
    value: Optional[int] = Field(None, description="Optional value")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "test",
                "value": 123
            }
        }
```

## Error Handling

```python
from fastapi import HTTPException

@app.get("/api/resource/{id}")
def get_resource(id: str):
    resource = service.get(id)
    if not resource:
        raise HTTPException(status_code=404, detail=f"Resource {id} not found")
    return resource
```

## Environment Variables

```python
import os

PORT = int(os.environ.get("PORT", 8080))
API_KEY = os.environ.get("API_KEY")
ENVIRONMENT = os.environ.get("ENVIRONMENT", "local")
```

## Dependencies

Minimal:

```txt
fastapi==0.115.0
uvicorn==0.32.0
pydantic==2.9.2
```

## Using Reusables

```python
# Add to path first (see main.py setup)
from reusables.python.redis import get_redis_client
from reusables.python.gemini import generate_text

# Use in routes
@app.get("/api/cached-data")
def get_cached():
    redis = get_redis_client()
    data = redis.get("key")
    return {"data": data}
```

## CORS (if needed)

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Running Locally

```python
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
```

Run: `python api/main.py`

## Docs

FastAPI auto-generates docs at `/api/docs`

## Do Not

- Do not put routes at `/` - reserve for dashboard
- Do not commit `.env` files
- Do not use blocking operations - use `async def` if needed
- Do not forget type hints on route functions

