"""
Log data models for Komfyrvakt.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum


class LogLevel(str, Enum):
    """Log severity levels."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class LogEntry(BaseModel):
    """
    Log entry model.
    
    Example:
        {
          "message": "Temperature reading",
          "level": "info",
          "group": "restaurant-a:fridge-1",
          "tags": ["temperature", "monitoring"],
          "data": {"temperature": 4.2},
          "timestamp": "2025-11-12T20:15:30Z",
          "source": "sensor-001"
        }
    """
    message: str = Field(..., description="Log message")
    level: LogLevel = Field(default=LogLevel.INFO, description="Log severity level")
    group: Optional[str] = Field(default=None, description="Group identifier (e.g., 'service:api', 'project:obsero:prod', 'tenant-123')")
    tags: List[str] = Field(default_factory=list, description="Tags for filtering")
    data: Optional[Dict[str, Any]] = Field(default=None, description="Additional structured data")
    timestamp: Optional[datetime] = Field(default=None, description="Log timestamp (auto-generated if not provided)")
    source: Optional[str] = Field(default=None, description="Source identifier (e.g., sensor ID, service name)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Temperature too high",
                "level": "warning",
                "group": "restaurant-a:fridge-1",
                "tags": ["temperature", "alert"],
                "data": {"temperature": 8.5, "threshold": 6.0},
                "timestamp": "2025-11-12T20:15:30Z",
                "source": "sensor-temp-001"
            }
        }


class StoredLog(BaseModel):
    """
    Log entry as stored in Redis (includes generated ID).
    """
    id: str = Field(..., description="Unique log ID")
    message: str
    level: LogLevel
    group: Optional[str] = None
    tags: List[str]
    data: Optional[Dict[str, Any]] = None
    timestamp: datetime
    source: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "log_20251112201530_abc123",
                "message": "Temperature too high",
                "level": "warning",
                "group": "restaurant-a:fridge-1",
                "tags": ["temperature", "alert"],
                "data": {"temperature": 8.5},
                "timestamp": "2025-11-12T20:15:30Z",
                "source": "sensor-temp-001"
            }
        }


class LogQuery(BaseModel):
    """Query parameters for fetching logs."""
    group: Optional[str] = Field(default=None, description="Filter by group (exact match or prefix with *)")
    tags: Optional[List[str]] = Field(default=None, description="Filter by tags (OR logic)")
    level: Optional[LogLevel] = Field(default=None, description="Filter by minimum severity")
    since: Optional[datetime] = Field(default=None, description="Logs after this timestamp")
    until: Optional[datetime] = Field(default=None, description="Logs before this timestamp")
    source: Optional[str] = Field(default=None, description="Filter by source")
    limit: int = Field(default=100, ge=1, le=1000, description="Max number of logs to return")

