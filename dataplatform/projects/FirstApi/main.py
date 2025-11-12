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

from reusables.python.common import get_greeting, get_library_info
from reusables.python.redis import get_redis_client, make_key

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


@app.get("/redis/test")
def redis_test():
    """Test Redis connection and demonstrate shared Redis client."""
    try:
        r = get_redis_client()
        
        # Test basic operations
        test_key = make_key('firstapi', 'test', 'hello')
        r.set(test_key, 'Hello from FirstApi via shared Redis!')
        value = r.get(test_key)
        
        # Get some stats
        info = r.info('server')
        
        return {
            "status": "success",
            "redis_connected": True,
            "test_key": test_key,
            "test_value": value,
            "redis_version": info.get('redis_version'),
            "message": "Successfully connected to shared Redis server!"
        }
    except Exception as e:
        return {
            "status": "error",
            "redis_connected": False,
            "error": str(e)
        }


@app.post("/redis/set/{key}")
def redis_set(key: str, value: str):
    """Set a value in Redis with namespaced key."""
    try:
        r = get_redis_client()
        namespaced_key = make_key('firstapi', 'data', key)
        r.set(namespaced_key, value)
        
        return {
            "status": "success",
            "key": namespaced_key,
            "value": value
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/redis/get/{key}")
def redis_get(key: str):
    """Get a value from Redis with namespaced key."""
    try:
        r = get_redis_client()
        namespaced_key = make_key('firstapi', 'data', key)
        value = r.get(namespaced_key)
        
        if value is None:
            return {
                "status": "not_found",
                "key": namespaced_key,
                "value": None
            }
        
        return {
            "status": "success",
            "key": namespaced_key,
            "value": value
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}


if __name__ == "__main__":
    import uvicorn
    # Cloud Run sets PORT env variable
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)

