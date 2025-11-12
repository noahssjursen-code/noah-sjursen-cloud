"""
Redis client for Noah Sjursen Cloud.
Shared Redis connection and utilities used across all services.
"""

import os
import redis
from typing import Optional, Any, List, Dict
import json


class RedisClient:
    """
    Shared Redis client with automatic environment-based configuration.
    
    Usage:
        from reusables.redis_client import get_redis_client
        
        r = get_redis_client()
        r.set('key', 'value')
        value = r.get('key')
    """
    
    _instance: Optional[redis.Redis] = None
    
    @classmethod
    def get_client(cls) -> redis.Redis:
        """
        Get or create Redis client singleton.
        
        Environment variables:
            REDIS_HOST: Redis server host (default: 34.66.188.104 for local, 10.128.0.3 for production)
            REDIS_PORT: Redis server port (default: 6379)
            ENVIRONMENT: 'local' or 'production' (default: 'local')
        
        Returns:
            Configured Redis client
        """
        if cls._instance is None:
            # Determine environment
            environment = os.getenv('ENVIRONMENT', 'local').lower()
            
            # Set host based on environment
            if environment == 'production':
                default_host = '10.128.0.3'  # Internal VPC IP
            else:
                default_host = '34.66.188.104'  # External IP for local development
            
            host = os.getenv('REDIS_HOST', default_host)
            port = int(os.getenv('REDIS_PORT', '6379'))
            
            cls._instance = redis.Redis(
                host=host,
                port=port,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5,
                retry_on_timeout=True,
                health_check_interval=30
            )
            
            # Test connection
            try:
                cls._instance.ping()
                print(f"✅ Connected to Redis at {host}:{port}")
            except redis.ConnectionError as e:
                print(f"❌ Failed to connect to Redis at {host}:{port}: {e}")
                raise
        
        return cls._instance
    
    @classmethod
    def reset(cls):
        """Reset the singleton instance (useful for testing)."""
        if cls._instance:
            cls._instance.close()
        cls._instance = None


# Convenience function
def get_redis_client() -> redis.Redis:
    """
    Get the shared Redis client.
    
    Returns:
        Configured Redis client
    """
    return RedisClient.get_client()


# ============================================================================
# KEY NAMING HELPERS
# ============================================================================

def make_key(service: str, *parts: str) -> str:
    """
    Create a namespaced Redis key.
    
    Args:
        service: Service name (e.g., 'firstapi', 'logger')
        *parts: Key parts to join
    
    Returns:
        Namespaced key (e.g., 'firstapi:cache:user:123')
    
    Example:
        key = make_key('firstapi', 'cache', 'user', '123')
        # Returns: 'firstapi:cache:user:123'
    """
    return ':'.join([service] + list(parts))


# ============================================================================
# CRUD OPERATIONS
# ============================================================================

def set_value(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set a value in Redis with optional TTL.
    
    Args:
        key: Redis key
        value: Value to store (will be JSON-serialized if not string)
        ttl: Time to live in seconds (None = no expiration)
    
    Returns:
        True if successful
    
    Example:
        set_value('user:123', {'name': 'Noah', 'age': 21}, ttl=3600)
    """
    r = get_redis_client()
    
    # Serialize complex objects
    if not isinstance(value, (str, int, float)):
        value = json.dumps(value)
    
    if ttl:
        return r.setex(key, ttl, value)
    else:
        return r.set(key, value)


def get_value(key: str, default: Any = None) -> Any:
    """
    Get a value from Redis.
    
    Args:
        key: Redis key
        default: Default value if key doesn't exist
    
    Returns:
        Value (will attempt JSON deserialization)
    
    Example:
        user = get_value('user:123')
    """
    r = get_redis_client()
    value = r.get(key)
    
    if value is None:
        return default
    
    # Try to deserialize JSON
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def delete_key(key: str) -> int:
    """
    Delete a key from Redis.
    
    Args:
        key: Redis key to delete
    
    Returns:
        Number of keys deleted (0 or 1)
    
    Example:
        delete_key('user:123')
    """
    r = get_redis_client()
    return r.delete(key)


def exists(key: str) -> bool:
    """
    Check if a key exists in Redis.
    
    Args:
        key: Redis key
    
    Returns:
        True if key exists
    
    Example:
        if exists('user:123'):
            print('User exists')
    """
    r = get_redis_client()
    return r.exists(key) > 0


def get_ttl(key: str) -> int:
    """
    Get the time-to-live of a key in seconds.
    
    Args:
        key: Redis key
    
    Returns:
        TTL in seconds (-1 = no expiration, -2 = key doesn't exist)
    
    Example:
        ttl = get_ttl('session:abc123')
    """
    r = get_redis_client()
    return r.ttl(key)


# ============================================================================
# BULK OPERATIONS
# ============================================================================

def set_many(mapping: Dict[str, Any], ttl: Optional[int] = None) -> bool:
    """
    Set multiple key-value pairs at once.
    
    Args:
        mapping: Dictionary of key-value pairs
        ttl: Optional TTL for all keys
    
    Returns:
        True if successful
    
    Example:
        set_many({
            'user:1': {'name': 'Noah'},
            'user:2': {'name': 'Alice'}
        }, ttl=3600)
    """
    r = get_redis_client()
    
    # Serialize all values
    serialized = {}
    for key, value in mapping.items():
        if not isinstance(value, (str, int, float)):
            value = json.dumps(value)
        serialized[key] = value
    
    result = r.mset(serialized)
    
    # Set TTL if provided
    if ttl and result:
        for key in serialized.keys():
            r.expire(key, ttl)
    
    return result


def get_many(keys: List[str]) -> Dict[str, Any]:
    """
    Get multiple values at once.
    
    Args:
        keys: List of Redis keys
    
    Returns:
        Dictionary of key-value pairs (missing keys are excluded)
    
    Example:
        users = get_many(['user:1', 'user:2', 'user:3'])
    """
    r = get_redis_client()
    values = r.mget(keys)
    
    result = {}
    for key, value in zip(keys, values):
        if value is not None:
            try:
                result[key] = json.loads(value)
            except (json.JSONDecodeError, TypeError):
                result[key] = value
    
    return result


def delete_many(keys: List[str]) -> int:
    """
    Delete multiple keys at once.
    
    Args:
        keys: List of Redis keys to delete
    
    Returns:
        Number of keys deleted
    
    Example:
        count = delete_many(['user:1', 'user:2', 'user:3'])
    """
    r = get_redis_client()
    if not keys:
        return 0
    return r.delete(*keys)


# ============================================================================
# PATTERN MATCHING & INVALIDATION
# ============================================================================

def find_keys(pattern: str, limit: int = 1000) -> List[str]:
    """
    Find keys matching a pattern.
    
    Args:
        pattern: Redis pattern (e.g., 'user:*', 'cache:*:profile')
        limit: Maximum number of keys to return
    
    Returns:
        List of matching keys
    
    Example:
        user_keys = find_keys('user:*')
        cache_keys = find_keys('firstapi:cache:*')
    
    Warning: Use with caution on large datasets. Consider using SCAN instead.
    """
    r = get_redis_client()
    return [key for key in r.scan_iter(match=pattern, count=limit)]


def invalidate_pattern(pattern: str) -> int:
    """
    Delete all keys matching a pattern.
    
    Args:
        pattern: Redis pattern (e.g., 'cache:*', 'session:user:123:*')
    
    Returns:
        Number of keys deleted
    
    Example:
        # Invalidate all cache for a user
        invalidate_pattern('cache:user:123:*')
        
        # Invalidate all sessions
        invalidate_pattern('session:*')
    
    Warning: This scans all keys. Use sparingly in production.
    """
    keys = find_keys(pattern)
    if keys:
        return delete_many(keys)
    return 0


def purge_cache(service: Optional[str] = None) -> int:
    """
    Purge cache entries, optionally filtered by service.
    
    Args:
        service: Service name to purge cache for (None = all cache)
    
    Returns:
        Number of keys deleted
    
    Example:
        # Purge all FirstApi cache
        purge_cache('firstapi')
        
        # Purge all cache
        purge_cache()
    """
    if service:
        pattern = f"{service}:cache:*"
    else:
        pattern = "*:cache:*"
    
    return invalidate_pattern(pattern)


# ============================================================================
# CACHE HELPERS
# ============================================================================

def cache_get(key: str) -> Optional[Any]:
    """
    Get a cached value (alias for get_value with None default).
    
    Args:
        key: Cache key
    
    Returns:
        Cached value or None
    
    Example:
        user = cache_get('cache:user:123')
    """
    return get_value(key, default=None)


def cache_set(key: str, value: Any, ttl: int = 3600) -> bool:
    """
    Set a cached value with default 1-hour TTL.
    
    Args:
        key: Cache key
        value: Value to cache
        ttl: Time to live in seconds (default: 3600 = 1 hour)
    
    Returns:
        True if successful
    
    Example:
        cache_set('cache:user:123', user_data, ttl=1800)
    """
    return set_value(key, value, ttl=ttl)


# ============================================================================
# INCREMENT/DECREMENT (Counters)
# ============================================================================

def increment(key: str, amount: int = 1) -> int:
    """
    Increment a counter.
    
    Args:
        key: Redis key
        amount: Amount to increment by (default: 1)
    
    Returns:
        New value after increment
    
    Example:
        views = increment('page:home:views')
        count = increment('api:requests:total', amount=1)
    """
    r = get_redis_client()
    return r.incrby(key, amount)


def decrement(key: str, amount: int = 1) -> int:
    """
    Decrement a counter.
    
    Args:
        key: Redis key
        amount: Amount to decrement by (default: 1)
    
    Returns:
        New value after decrement
    
    Example:
        remaining = decrement('tokens:user:123')
    """
    r = get_redis_client()
    return r.decrby(key, amount)


# ============================================================================
# HASH OPERATIONS (for structured data)
# ============================================================================

def hash_set(key: str, field: str, value: Any) -> int:
    """
    Set a field in a Redis hash.
    
    Args:
        key: Hash key
        field: Field name
        value: Field value
    
    Returns:
        1 if new field, 0 if updated
    
    Example:
        hash_set('user:123', 'name', 'Noah')
        hash_set('user:123', 'age', 21)
    """
    r = get_redis_client()
    if not isinstance(value, (str, int, float)):
        value = json.dumps(value)
    return r.hset(key, field, value)


def hash_get(key: str, field: str) -> Optional[Any]:
    """
    Get a field from a Redis hash.
    
    Args:
        key: Hash key
        field: Field name
    
    Returns:
        Field value or None
    
    Example:
        name = hash_get('user:123', 'name')
    """
    r = get_redis_client()
    value = r.hget(key, field)
    
    if value is None:
        return None
    
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return value


def hash_get_all(key: str) -> Dict[str, Any]:
    """
    Get all fields from a Redis hash.
    
    Args:
        key: Hash key
    
    Returns:
        Dictionary of all field-value pairs
    
    Example:
        user = hash_get_all('user:123')
        # {'name': 'Noah', 'age': 21}
    """
    r = get_redis_client()
    data = r.hgetall(key)
    
    # Try to deserialize JSON values
    result = {}
    for field, value in data.items():
        try:
            result[field] = json.loads(value)
        except (json.JSONDecodeError, TypeError):
            result[field] = value
    
    return result

