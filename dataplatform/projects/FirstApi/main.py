"""
FirstApi - A simple test API for Noah Sjursen Cloud.
Demonstrates Cloud Run source deployment and reusables pattern.
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
import sys
import os

# Add parent directory to path to import reusables
# In deployment, deploy script copies reusables temporarily
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from reusables.common import get_greeting, get_library_info

app = FastAPI(
    title="FirstApi",
    description="Noah Sjursen Cloud - First Test API",
    version="1.0.0"
)


@app.get("/")
def root():
    """Root endpoint - demonstrates importing from reusables."""
    message = get_greeting("FirstApi")
    return {
        "message": message,
        "status": "success",
        "api": "FirstApi"
    }


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.get("/info")
def info():
    """Get information about this API and the reusables library."""
    library_info = get_library_info()
    return {
        "api": {
            "name": "FirstApi",
            "version": "1.0.0",
            "description": "First test API for Noah Sjursen Cloud"
        },
        "reusables": library_info,
        "message": "Successfully imported shared utilities from reusables!"
    }


if __name__ == "__main__":
    import uvicorn
    # Cloud Run sets PORT env variable
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

