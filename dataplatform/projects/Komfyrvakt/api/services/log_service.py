"""
Log storage and retrieval service for Komfyrvakt.
Handles Redis operations for log entries.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))  # For reusables

from datetime import datetime, timedelta
from typing import List, Optional
import json
import uuid

from reusables.python.redis import get_redis_client, find_keys
from models.log import LogEntry, StoredLog, LogLevel, LogQuery


class LogService:
    """Service for managing logs in Redis."""
    
    KEY_PREFIX = "komfyrvakt:logs"
    INDEX_PREFIX = "komfyrvakt:index"
    
    @staticmethod
    def _generate_log_id(timestamp: datetime) -> str:
        """Generate unique log ID with timestamp."""
        ts_str = timestamp.strftime('%Y%m%d%H%M%S')
        random_suffix = uuid.uuid4().hex[:8]
        return f"log_{ts_str}_{random_suffix}"
    
    @staticmethod
    def _make_log_key(log_id: str) -> str:
        """Create Redis key for log entry."""
        return f"{LogService.KEY_PREFIX}:{log_id}"
    
    @staticmethod
    def _make_tag_index_key(tag: str, log_id: str) -> str:
        """Create Redis key for tag index."""
        return f"{LogService.INDEX_PREFIX}:tag:{tag}:{log_id}"
    
    @classmethod
    def store_log(cls, log_entry: LogEntry, retention_hours: int = 48) -> StoredLog:
        """
        Store a log entry in Redis.
        
        Args:
            log_entry: Log entry to store
            retention_hours: How long to keep the log
        
        Returns:
            Stored log with generated ID
        """
        r = get_redis_client()
        
        # Generate timestamp if not provided
        if log_entry.timestamp is None:
            log_entry.timestamp = datetime.utcnow()
        
        # Generate unique ID
        log_id = cls._generate_log_id(log_entry.timestamp)
        
        # Create stored log
        stored_log = StoredLog(
            id=log_id,
            message=log_entry.message,
            level=log_entry.level,
            group=log_entry.group,
            tags=log_entry.tags,
            data=log_entry.data,
            timestamp=log_entry.timestamp,
            source=log_entry.source
        )
        
        # Store in Redis with TTL
        log_key = cls._make_log_key(log_id)
        ttl_seconds = retention_hours * 3600
        r.setex(log_key, ttl_seconds, stored_log.model_dump_json())
        
        # Create tag indexes for fast filtering
        for tag in log_entry.tags:
            tag_key = cls._make_tag_index_key(tag, log_id)
            r.setex(tag_key, ttl_seconds, log_id)
        
        # Create group index for fast filtering
        if log_entry.group:
            group_key = f"{cls.INDEX_PREFIX}:group:{log_entry.group}:{log_id}"
            r.setex(group_key, ttl_seconds, log_id)
        
        return stored_log
    
    @classmethod
    def get_log(cls, log_id: str) -> Optional[StoredLog]:
        """
        Get a specific log by ID.
        
        Args:
            log_id: Log ID
        
        Returns:
            Stored log or None if not found
        """
        r = get_redis_client()
        log_key = cls._make_log_key(log_id)
        log_json = r.get(log_key)
        
        if log_json is None:
            return None
        
        return StoredLog.model_validate_json(log_json)
    
    @classmethod
    def query_logs(cls, query: LogQuery) -> List[StoredLog]:
        """
        Query logs based on filters.
        
        Args:
            query: Query parameters
        
        Returns:
            List of matching logs
        """
        r = get_redis_client()
        
        # Get log IDs based on filters
        log_ids = set()
        
        # Filter by group first (most specific)
        if query.group:
            if query.group.endswith('*'):
                # Prefix match (e.g., "restaurant-a:*")
                group_prefix = query.group[:-1]
                group_pattern = f"{cls.INDEX_PREFIX}:group:{group_prefix}*"
            else:
                # Exact match
                group_pattern = f"{cls.INDEX_PREFIX}:group:{query.group}:*"
            
            group_keys = find_keys(group_pattern)
            for key in group_keys:
                log_id = key.split(':')[-1]
                log_ids.add(log_id)
        
        # Filter by tags (OR logic)
        elif query.tags:
            for tag in query.tags:
                tag_pattern = f"{cls.INDEX_PREFIX}:tag:{tag}:*"
                tag_keys = find_keys(tag_pattern)
                for key in tag_keys:
                    log_id = key.split(':')[-1]
                    log_ids.add(log_id)
        
        # No filters - get all logs
        else:
            log_pattern = f"{cls.KEY_PREFIX}:*"
            log_keys = find_keys(log_pattern, limit=query.limit * 2)
            log_ids = set(key.replace(f"{cls.KEY_PREFIX}:", '') for key in log_keys)
        
        # Fetch logs
        logs = []
        for log_id in log_ids:
            log = cls.get_log(log_id)
            if log is None:
                continue
            
            # Apply additional filters
            if query.level and log.level.value < query.level.value:
                continue
            
            if query.since and log.timestamp < query.since:
                continue
            
            if query.until and log.timestamp > query.until:
                continue
            
            if query.source and log.source != query.source:
                continue
            
            # If tags were specified, ensure log has at least one matching tag
            if query.tags and not any(tag in log.tags for tag in query.tags):
                continue
            
            logs.append(log)
            
            if len(logs) >= query.limit:
                break
        
        # Sort by timestamp (newest first)
        logs.sort(key=lambda x: x.timestamp, reverse=True)
        
        return logs[:query.limit]
    
    @classmethod
    def get_groups(cls) -> list:
        """
        Get all unique groups from stored logs.
        
        Returns:
            List of unique group identifiers
        """
        r = get_redis_client()
        
        # Find all group index keys
        group_pattern = f"{cls.INDEX_PREFIX}:group:*"
        group_keys = find_keys(group_pattern, limit=10000)
        
        # Extract unique groups
        groups = set()
        for key in group_keys:
            # Key format: komfyrvakt:index:group:{group_name}:{log_id}
            parts = key.split(':')
            # Get everything between 'group' and the log_id (last part)
            if len(parts) >= 4:
                # Reconstruct group name (could have colons in it)
                group = ':'.join(parts[3:-1])
                if group:
                    groups.add(group)
        
        # Sort groups alphabetically
        return sorted(list(groups))
    
    @classmethod
    def get_stats(cls) -> dict:
        """
        Get statistics about stored logs.
        
        Returns:
            Dictionary with log counts and metadata
        """
        r = get_redis_client()
        
        # Count total logs
        log_pattern = f"{cls.KEY_PREFIX}:*"
        log_keys = find_keys(log_pattern)
        
        return {
            "total_logs": len(log_keys),
            "storage": "redis",
            "retention_hours": 48  # Could read from config
        }
    
    @classmethod
    def purge_logs(cls, group: Optional[str] = None) -> dict:
        """
        Purge logs from Redis.
        
        Args:
            group: Optional group to purge (None = purge all logs)
        
        Returns:
            Dictionary with purge results
        """
        r = get_redis_client()
        
        if group:
            # Purge specific group
            if group.endswith('*'):
                # Prefix match
                group_prefix = group[:-1]
                pattern = f"{cls.INDEX_PREFIX}:group:{group_prefix}*"
            else:
                # Exact match
                pattern = f"{cls.INDEX_PREFIX}:group:{group}:*"
            
            # Find log IDs for this group
            group_keys = find_keys(pattern)
            log_ids = [key.split(':')[-1] for key in group_keys]
            
            # Delete logs and indexes
            deleted = 0
            for log_id in log_ids:
                log_key = cls._make_log_key(log_id)
                deleted += r.delete(log_key)
            
            # Delete group indexes
            for key in group_keys:
                r.delete(key)
            
            # Delete tag indexes for these logs
            tag_pattern = f"{cls.INDEX_PREFIX}:tag:*"
            tag_keys = find_keys(tag_pattern)
            for key in tag_keys:
                if key.split(':')[-1] in log_ids:
                    r.delete(key)
            
            return {
                "purged": deleted,
                "group": group,
                "scope": "group"
            }
        else:
            # Purge ALL logs
            log_pattern = f"{cls.KEY_PREFIX}:*"
            index_pattern = f"{cls.INDEX_PREFIX}:*"
            
            log_keys = find_keys(log_pattern, limit=10000)
            index_keys = find_keys(index_pattern, limit=10000)
            
            deleted_logs = r.delete(*log_keys) if log_keys else 0
            deleted_indexes = r.delete(*index_keys) if index_keys else 0
            
            return {
                "purged": deleted_logs,
                "indexes_cleared": deleted_indexes,
                "scope": "all"
            }

