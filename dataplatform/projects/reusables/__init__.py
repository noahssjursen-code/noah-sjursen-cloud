"""
Reusable utilities for Noah Sjursen Cloud projects.
Shared across multiple services - similar to C# class libraries.

Organization:
    reusables.redis - Redis client and utilities
    reusables.common - General utilities
"""

__version__ = "0.1.0"

# Convenient top-level imports
from .redis import get_redis_client, cache_get, cache_set, make_key
from .common import get_greeting, get_library_info

__all__ = [
    'get_redis_client',
    'cache_get',
    'cache_set',
    'make_key',
    'get_greeting',
    'get_library_info',
]

