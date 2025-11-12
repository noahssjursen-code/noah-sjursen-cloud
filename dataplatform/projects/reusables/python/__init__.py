"""
Python utilities for Noah Sjursen Cloud.
"""

# Convenient imports
from .redis import get_redis_client, cache_get, cache_set, make_key
from .common import get_greeting, get_library_info
from .gemini import generate_text, strip_code_blocks

__all__ = [
    'get_redis_client',
    'cache_get',
    'cache_set',
    'make_key',
    'get_greeting',
    'get_library_info',
    'generate_text',
    'strip_code_blocks',
]

