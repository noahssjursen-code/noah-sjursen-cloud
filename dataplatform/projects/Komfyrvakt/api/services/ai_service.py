"""
AI analysis service for Komfyrvakt.
Handles log analysis using Gemini AI with caching.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from typing import List, Dict, Any, Optional
import json
from datetime import datetime

from reusables.python.gemini import generate_text
from reusables.python.redis import get_redis_client, cache_get, cache_set
from models.log import StoredLog


class AIService:
    """Service for AI-powered log analysis."""
    
    CACHE_PREFIX = "komfyrvakt:ai:analysis"
    CACHE_TTL = 3600  # 1 hour
    
    @classmethod
    def _make_cache_key(cls, group: Optional[str], cache_id: str) -> str:
        """Create cache key for analysis results."""
        if group:
            return f"{cls.CACHE_PREFIX}:{group}:{cache_id}"
        return f"{cls.CACHE_PREFIX}:all:{cache_id}"
    
    @classmethod
    def _aggregate_data(cls, logs: List[StoredLog]) -> Dict[str, Any]:
        """
        Aggregate data from logs dynamically based on data field types.
        
        Args:
            logs: List of log entries
        
        Returns:
            Aggregated statistics by data field
        """
        aggregation = {
            "total_logs": len(logs),
            "level_counts": {},
            "tag_counts": {},
            "data_fields": {}
        }
        
        # Count by level
        for log in logs:
            level = log.level.value
            aggregation["level_counts"][level] = aggregation["level_counts"].get(level, 0) + 1
        
        # Count by tags
        for log in logs:
            for tag in log.tags:
                aggregation["tag_counts"][tag] = aggregation["tag_counts"].get(tag, 0) + 1
        
        # Aggregate data fields dynamically
        for log in logs:
            if log.data:
                for field, value in log.data.items():
                    if field not in aggregation["data_fields"]:
                        aggregation["data_fields"][field] = {
                            "type": type(value).__name__,
                            "values": [],
                            "count": 0
                        }
                    
                    field_data = aggregation["data_fields"][field]
                    field_data["count"] += 1
                    
                    # Aggregate based on type
                    if isinstance(value, (int, float)):
                        # Numeric - calculate stats
                        field_data["values"].append(value)
                        if len(field_data["values"]) == field_data["count"]:
                            # Calculate on last item
                            values = field_data["values"]
                            field_data["min"] = min(values)
                            field_data["max"] = max(values)
                            field_data["avg"] = sum(values) / len(values)
                    elif isinstance(value, str):
                        # String - count unique values
                        if "unique_values" not in field_data:
                            field_data["unique_values"] = set()
                        field_data["unique_values"].add(value)
        
        # Convert sets to lists for JSON serialization
        for field_data in aggregation["data_fields"].values():
            if "unique_values" in field_data:
                field_data["unique_values"] = list(field_data["unique_values"])
        
        return aggregation
    
    @classmethod
    def analyze_logs(
        cls,
        logs: List[StoredLog],
        group: Optional[str] = None,
        use_cache: bool = True,
        api_key: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Analyze logs using AI with caching.
        
        Args:
            logs: List of log entries to analyze
            group: Optional group identifier for cache key
            use_cache: Use cached results if available
            api_key: Gemini API key
        
        Returns:
            Analysis results with aggregated data and AI insights
        """
        # Generate cache key based on logs
        cache_id = f"{len(logs)}_{datetime.utcnow().strftime('%Y%m%d%H')}"  # Hour-based cache
        cache_key = cls._make_cache_key(group, cache_id)
        
        # Check cache first
        if use_cache:
            cached = cache_get(cache_key)
            if cached:
                return {
                    "status": "success",
                    "cached": True,
                    "analysis": cached
                }
        
        # Aggregate data dynamically
        aggregation = cls._aggregate_data(logs)
        
        # Format for AI analysis
        log_summary = []
        for log in logs[:50]:  # Limit to 50 most recent for AI
            log_summary.append(
                f"[{log.level.value.upper()}] {log.message}"
                + (f" | {log.data}" if log.data else "")
            )
        
        # Build AI prompt
        prompt = f"""Analyze these system logs and provide insights:

Total logs: {aggregation['total_logs']}
Level breakdown: {aggregation['level_counts']}
Data fields detected: {list(aggregation['data_fields'].keys())}

Recent logs:
{chr(10).join(log_summary[:20])}

Provide:
1. Brief summary of system status
2. Any anomalies or concerning patterns
3. Specific recommendations

Be concise and actionable."""
        
        # Generate AI analysis
        try:
            ai_insights = generate_text(
                prompt,
                api_key=api_key,
                temperature=0.3,
                strip_code_markers=True
            )
        except Exception as e:
            ai_insights = f"AI analysis unavailable: {str(e)}"
        
        # Combine results
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "group": group,
            "aggregation": aggregation,
            "ai_insights": ai_insights,
            "analyzed_logs": len(logs)
        }
        
        # Cache the result
        cache_set(cache_key, result, ttl=cls.CACHE_TTL)
        
        return {
            "status": "success",
            "cached": False,
            "analysis": result
        }

