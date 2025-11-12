"""
Redis utilities for Noah Sjursen Cloud.
"""

from .client import (
    # Core client
    get_redis_client,
    RedisClient,
    
    # Key helpers
    make_key,
    
    # CRUD operations
    set_value,
    get_value,
    delete_key,
    exists,
    get_ttl,
    
    # Bulk operations
    set_many,
    get_many,
    delete_many,
    
    # Pattern matching & invalidation
    find_keys,
    invalidate_pattern,
    purge_cache,
    
    # Cache helpers
    cache_get,
    cache_set,
    
    # Counters
    increment,
    decrement,
    
    # Hash operations
    hash_set,
    hash_get,
    hash_get_all,
)

__all__ = [
    # Core
    'get_redis_client',
    'RedisClient',
    
    # Key helpers
    'make_key',
    
    # CRUD
    'set_value',
    'get_value',
    'delete_key',
    'exists',
    'get_ttl',
    
    # Bulk
    'set_many',
    'get_many',
    'delete_many',
    
    # Pattern matching
    'find_keys',
    'invalidate_pattern',
    'purge_cache',
    
    # Cache
    'cache_get',
    'cache_set',
    
    # Counters
    'increment',
    'decrement',
    
    # Hash
    'hash_set',
    'hash_get',
    'hash_get_all',
]

