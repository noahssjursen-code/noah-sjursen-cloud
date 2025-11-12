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
    """Service for AI-powered log analysis with time series support."""
    
    CACHE_PREFIX_ANALYSIS = "komfyrvakt:ai:analysis"
    CACHE_PREFIX_TIMESERIES = "komfyrvakt:ai:timeseries"
    ANALYSIS_TTL = 7200  # 2 hours for AI reports
    TIMESERIES_TTL = 1800  # 30 minutes for time series data
    
    @classmethod
    def _make_cache_key(cls, prefix: str, group: Optional[str], cache_id: str) -> str:
        """Create cache key for analysis results."""
        if group:
            return f"{prefix}:{group}:{cache_id}"
        return f"{prefix}:all:{cache_id}"
    
    @classmethod
    def _generate_time_series(cls, logs: List[StoredLog]) -> Dict[str, Any]:
        """
        Generate time series data from logs.
        Groups logs by time intervals and extracts numeric fields.
        """
        from collections import defaultdict
        from datetime import datetime as dt
        
        # Group logs by minute
        time_series = defaultdict(lambda: {
            "timestamp": None,
            "count": 0,
            "levels": defaultdict(int),
            "data_points": defaultdict(list)
        })
        
        for log in logs:
            # Parse timestamp and round to minute
            try:
                # Handle various timestamp formats
                timestamp_str = log.timestamp
                if isinstance(timestamp_str, str):
                    timestamp_str = timestamp_str.replace('Z', '+00:00')
                    log_time = dt.fromisoformat(timestamp_str)
                else:
                    log_time = timestamp_str
                
                # Round to 5-minute intervals for better visualization
                minute = (log_time.minute // 5) * 5
                time_key = log_time.strftime(f'%Y-%m-%d %H:{minute:02d}:00')
            except Exception as e:
                print(f"Failed to parse timestamp {log.timestamp}: {e}")
                continue
            
            entry = time_series[time_key]
            if entry["timestamp"] is None:
                entry["timestamp"] = time_key
            
            entry["count"] += 1
            entry["levels"][log.level.value] += 1
            
            # Extract numeric data fields
            if log.data:
                for field, value in log.data.items():
                    if isinstance(value, (int, float)):
                        entry["data_points"][field].append(value)
        
        # Convert to sorted list and calculate averages
        result = []
        for time_key in sorted(time_series.keys()):
            entry = time_series[time_key]
            
            # Calculate averages for data points
            data_avg = {}
            for field, values in entry["data_points"].items():
                if values:
                    data_avg[field] = {
                        "min": min(values),
                        "max": max(values),
                        "avg": sum(values) / len(values),
                        "count": len(values)
                    }
            
            result.append({
                "timestamp": entry["timestamp"],
                "log_count": entry["count"],
                "levels": dict(entry["levels"]),
                "data": data_avg
            })
        
        return {
            "intervals": result,
            "total_intervals": len(result),
            "fields_tracked": list(data_avg.keys()) if result else []
        }
    
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
        # Generate cache keys based on time window, NOT log count
        # This ensures cache is reused even when new logs arrive
        cache_id = datetime.utcnow().strftime('%Y%m%d%H')  # Hour-based cache only
        analysis_cache_key = cls._make_cache_key(cls.CACHE_PREFIX_ANALYSIS, group, cache_id)
        timeseries_cache_key = cls._make_cache_key(cls.CACHE_PREFIX_TIMESERIES, group, cache_id)
        
        print(f"Cache check - use_cache={use_cache}, key={analysis_cache_key}")
        
        # Check analysis cache first
        if use_cache:
            cached = cache_get(analysis_cache_key)
            print(f"Cache lookup result: {type(cached)} - {bool(cached)}")
            if cached:
                print(f"✅ Using cached analysis for {group or 'all'}")
                return {
                    "status": "success",
                    "cached": True,
                    "analysis": cached
                }
            else:
                print(f"❌ No cache found for key: {analysis_cache_key}")
        
        print(f"🔄 Generating NEW analysis for {group or 'all'} ({len(logs)} logs)")
        
        # Generate or get cached time series
        time_series = None
        if use_cache:
            time_series = cache_get(timeseries_cache_key)
        
        if not time_series:
            time_series = cls._generate_time_series(logs)
            print(f"Generated time series: {time_series.get('total_intervals', 0)} intervals, fields: {time_series.get('fields_tracked', [])}")
            # Cache time series separately
            cache_set(timeseries_cache_key, time_series, ttl=cls.TIMESERIES_TTL)
        
        # Aggregate data dynamically
        aggregation = cls._aggregate_data(logs)
        
        # Format for AI analysis
        log_summary = []
        for log in logs[:50]:  # Limit to 50 most recent for AI
            log_summary.append(
                f"[{log.level.value.upper()}] {log.message}"
                + (f" | {log.data}" if log.data else "")
            )
        
        # Build AI prompt with time series data
        time_series_summary = ""
        if time_series and time_series.get('intervals'):
            intervals = time_series['intervals'][-20:]  # Last 20 intervals
            time_series_summary = f"""

Time Series Data (last {len(intervals)} intervals):
"""
            for interval in intervals:
                time_series_summary += f"\n{interval['timestamp']}: {interval['log_count']} logs"
                if interval['data']:
                    for field, stats in interval['data'].items():
                        time_series_summary += f" | {field}: {stats['avg']:.2f}"
        
        prompt = f"""You are analyzing system logs with time series data. Return a JSON object:

{{
  "summary": "Brief 1-2 sentence overview of system health based on trends",
  "severity": "normal|warning|critical",
  "findings": [
    {{"title": "Finding name", "description": "Details with temporal context", "severity": "info|warning|critical"}}
  ],
  "recommendations": [
    {{"action": "What to do", "priority": "low|medium|high"}}
  ]
}}

Analysis Data:
- Total logs: {aggregation['total_logs']}
- Time range: {time_series.get('total_intervals', 0)} intervals tracked
- Fields monitored: {', '.join(time_series.get('fields_tracked', []))}
- Log levels: {aggregation['level_counts']}
{time_series_summary}

Recent log samples:
{chr(10).join(log_summary[:10])}

Focus on:
1. Temporal trends (increasing/decreasing patterns)
2. Anomalies in time series
3. Correlation between fields
4. Rate of change

Return ONLY valid JSON. Be specific about time-based patterns."""
        
        # Generate AI analysis
        try:
            ai_response = generate_text(
                prompt,
                api_key=api_key,
                temperature=0.3,
                strip_code_markers=True
            )
            
            # Parse JSON response
            try:
                ai_insights = json.loads(ai_response)
            except json.JSONDecodeError:
                # Fallback if AI doesn't return valid JSON
                ai_insights = {
                    "summary": ai_response[:200],
                    "severity": "warning",
                    "findings": [{"title": "Analysis", "description": ai_response, "severity": "info"}],
                    "recommendations": []
                }
        except Exception as e:
            ai_insights = {
                "summary": f"AI analysis unavailable: {str(e)}",
                "severity": "warning",
                "findings": [],
                "recommendations": []
            }
        
        # Combine results
        result = {
            "timestamp": datetime.utcnow().isoformat(),
            "group": group,
            "aggregation": aggregation,
            "time_series": time_series,  # Include time series in response
            "ai_insights": ai_insights,
            "analyzed_logs": len(logs)
        }
        
        # Cache the analysis result (longer TTL)
        cache_success = cache_set(analysis_cache_key, result, ttl=cls.ANALYSIS_TTL)
        print(f"💾 Cached analysis: {cache_success}, key={analysis_cache_key}, TTL={cls.ANALYSIS_TTL}s")
        
        return {
            "status": "success",
            "cached": False,
            "analysis": result
        }

