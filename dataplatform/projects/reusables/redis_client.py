"""
Redis client for Noah Sjursen Cloud.
Shared Redis connection used across all services.
"""

import os
import redis
from typing import Optional


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
            REDIS_HOST: Redis server host (default: 34.66.188.104 for local, 10.128.0.2 for production)
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


# Key naming helpers
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

