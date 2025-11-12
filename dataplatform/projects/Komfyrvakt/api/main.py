"""
Komfyrvakt - Simple logging service with AI analytics
Main FastAPI application
"""

import sys
import os

# Add parent directories to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))  # For reusables
sys.path.insert(0, os.path.dirname(__file__))  # For local modules

from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from typing import List, Optional
from datetime import datetime

from models.log import LogEntry, StoredLog, LogLevel, LogQuery
from services.log_service import LogService
from services.ai_service import AIService
from utils.auth import verify_api_key
from config.settings import settings

# Ensure API key is set
settings.ensure_api_key()

# Debug: Check if Gemini key is loaded
if settings.has_ai_enabled():
    print(f"✅ Gemini API key loaded (ends with: ...{settings.GEMINI_API_KEY[-8:]})")
else:
    print("⚠️  No Gemini API key found - AI features disabled")

app = FastAPI(
    title="Komfyrvakt",
    description="Simple, self-hostable logging service with AI analytics",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)


@app.get("/api")
def root():
    """API root endpoint."""
    return {
        "service": "Komfyrvakt",
        "version": "0.1.0",
        "description": "Simple logging service with AI analytics",
        "tagline": "Preventing infrastructure fires 🔥"
    }


@app.get("/api/health")
def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Komfyrvakt"
    }


@app.post("/api/logs", response_model=StoredLog, dependencies=[Depends(verify_api_key)])
def post_log(log: LogEntry):
    """
    Ingest a log entry.
    
    Requires API key in Authorization header:
        Authorization: Bearer kmf_your_api_key
    """
    try:
        stored_log = LogService.store_log(log, retention_hours=settings.LOG_RETENTION_HOURS)
        return stored_log
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store log: {str(e)}")


@app.post("/api/logs/batch", dependencies=[Depends(verify_api_key)])
def post_logs_batch(logs: List[LogEntry]):
    """
    Ingest multiple log entries in a single request.
    
    Requires API key in Authorization header:
        Authorization: Bearer kmf_your_api_key
    """
    try:
        stored_logs = []
        for idx, log in enumerate(logs):
            if idx == 0:  # Debug first log
                print(f"First log timestamp: {log.timestamp}, type: {type(log.timestamp)}")
            stored_log = LogService.store_log(log, retention_hours=settings.LOG_RETENTION_HOURS)
            stored_logs.append(stored_log)
        
        print(f"Batch ingested {len(stored_logs)} logs with timestamps ranging: {stored_logs[0].timestamp} to {stored_logs[-1].timestamp}")
        
        return {
            "status": "success",
            "ingested": len(stored_logs),
            "logs": stored_logs
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to store logs: {str(e)}")


@app.get("/api/logs", response_model=List[StoredLog], dependencies=[Depends(verify_api_key)])
def get_logs(
    group: Optional[str] = Query(default=None, description="Filter by group (use * for prefix match)"),
    tags: Optional[str] = Query(default=None, description="Comma-separated tags to filter by"),
    level: Optional[LogLevel] = Query(default=None, description="Minimum log level"),
    since: Optional[str] = Query(default=None, description="ISO timestamp - logs after this time"),
    until: Optional[str] = Query(default=None, description="ISO timestamp - logs before this time"),
    source: Optional[str] = Query(default=None, description="Filter by source"),
    limit: int = Query(default=100, ge=1, le=1000, description="Maximum number of logs")
):
    """
    Query logs with optional filters.
    
    Requires API key in Authorization header:
        Authorization: Bearer kmf_your_api_key
    
    Examples:
        /logs?group=restaurant-a:fridge-1
        /logs?group=service:api:*
        /logs?tags=fridge-1,warning&limit=50
        /logs?level=error&since=2025-11-12T00:00:00Z
        /logs?source=sensor-001
    """
    # Parse query parameters
    tag_list = tags.split(',') if tags else None
    since_dt = datetime.fromisoformat(since.replace('Z', '+00:00')) if since else None
    until_dt = datetime.fromisoformat(until.replace('Z', '+00:00')) if until else None
    
    query = LogQuery(
        group=group,
        tags=tag_list,
        level=level,
        since=since_dt,
        until=until_dt,
        source=source,
        limit=limit
    )
    
    try:
        logs = LogService.query_logs(query)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to query logs: {str(e)}")


@app.get("/api/logs/{log_id}", response_model=StoredLog, dependencies=[Depends(verify_api_key)])
def get_log_by_id(log_id: str):
    """
    Get a specific log by ID.
    
    Requires API key in Authorization header.
    """
    log = LogService.get_log(log_id)
    if log is None:
        raise HTTPException(status_code=404, detail=f"Log {log_id} not found")
    return log


@app.get("/api/groups", dependencies=[Depends(verify_api_key)])
def get_groups():
    """
    Get all unique groups from logs.
    
    Requires API key in Authorization header.
    
    Returns list of group identifiers for filtering.
    """
    try:
        groups = LogService.get_groups()
        return {
            "status": "success",
            "groups": groups,
            "count": len(groups)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get groups: {str(e)}")


@app.get("/api/stats", dependencies=[Depends(verify_api_key)])
def get_stats():
    """
    Get statistics about stored logs.
    
    Requires API key in Authorization header.
    """
    try:
        stats = LogService.get_stats()
        return {
            "status": "success",
            "stats": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get stats: {str(e)}")


@app.delete("/api/purge", dependencies=[Depends(verify_api_key)])
def purge_logs(
    group: Optional[str] = Query(default=None, description="Group to purge (use * for prefix, omit to purge ALL)")
):
    """
    Purge logs from storage.
    
    Requires API key in Authorization header.
    
    Examples:
        DELETE /purge                          # Purge ALL logs (⚠️ dangerous!)
        DELETE /purge?group=restaurant-a       # Purge specific group
        DELETE /purge?group=restaurant-a:*     # Purge all restaurant-a logs
    
    ⚠️ Warning: This operation cannot be undone!
    """
    try:
        result = LogService.purge_logs(group)
        return {
            "status": "success",
            "result": result
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to purge logs: {str(e)}")


@app.post("/api/analyze", dependencies=[Depends(verify_api_key)])
def analyze_logs(
    group: Optional[str] = Query(default=None, description="Group to analyze (None = all logs)"),
    refresh: bool = Query(default=False, description="Force new analysis (ignore cache)")
):
    """
    Analyze logs using AI with dynamic data aggregation.
    
    Requires API key in Authorization header.
    
    Features:
    - Dynamically aggregates data fields from log.data
    - Provides AI-powered insights using Gemini
    - Caches results for 1 hour (unless refresh=true)
    
    Examples:
        POST /api/analyze                        # Analyze all logs
        POST /api/analyze?group=restaurant-a:*   # Analyze specific group
        POST /api/analyze?refresh=true           # Force new analysis
    """
    try:
        print(f"📊 /api/analyze - group={group}, refresh={refresh}, use_cache={not refresh}")
        
        # Build query for logs
        query = LogQuery(
            group=group,
            limit=1000  # Analyze up to 1000 logs
        )
        
        # Fetch logs
        logs = LogService.query_logs(query)
        
        if not logs:
            return {
                "status": "success",
                "cached": False,
                "analysis": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "group": group,
                    "aggregation": {
                        "total_logs": 0,
                        "level_counts": {},
                        "tag_counts": {},
                        "data_fields": {}
                    },
                    "ai_insights": "No logs found to analyze in this group.",
                    "analyzed_logs": 0
                }
            }
        
        # Check if AI is enabled
        if not settings.has_ai_enabled():
            # Still return aggregation, just no AI insights
            aggregation = AIService._aggregate_data(logs)
            return {
                "status": "success",
                "cached": False,
                "analysis": {
                    "timestamp": datetime.utcnow().isoformat(),
                    "group": group,
                    "aggregation": aggregation,
                    "ai_insights": "AI analysis not configured. Set GEMINI_API_KEY in .env file to enable AI insights.",
                    "analyzed_logs": len(logs)
                }
            }
        
        # Analyze with AI
        result = AIService.analyze_logs(
            logs,
            group=group,
            use_cache=not refresh,
            api_key=settings.GEMINI_API_KEY
        )
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to analyze logs: {str(e)}")


# Serve dashboard static files (mounted AFTER all API routes)
dashboard_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard', 'build')
if os.path.exists(dashboard_path):
    app.mount("/", StaticFiles(directory=dashboard_path, html=True), name="dashboard")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    
    print("\n" + "=" * 50)
    print("🔥 Starting Komfyrvakt...")
    print("=" * 50)
    
    uvicorn.run(app, host="0.0.0.0", port=port)

