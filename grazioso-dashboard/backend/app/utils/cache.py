"""
Caching layer with Redis backend and in-memory fallback.
"""
import json
import hashlib
import logging
from typing import Any, Optional, Callable
from functools import wraps
from app.core.redis import get_redis_client, is_redis_available
from app.core.config import settings

logger = logging.getLogger(__name__)

# In-memory cache fallback
_memory_cache: dict = {}
_memory_cache_ttl: dict = {}
import time


def _generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """
    Generate a cache key from prefix and arguments.
    
    Args:
        prefix: Cache key prefix
        *args: Positional arguments
        **kwargs: Keyword arguments
        
    Returns:
        Cache key string
    """
    # Create a deterministic string representation
    key_parts = [prefix]
    if args:
        key_parts.extend(str(arg) for arg in args)
    if kwargs:
        sorted_kwargs = sorted(kwargs.items())
        key_parts.extend(f"{k}={v}" for k, v in sorted_kwargs)
    
    key_string = ":".join(key_parts)
    # Hash for consistent key length
    return hashlib.md5(key_string.encode()).hexdigest()


def get_from_cache(key: str) -> Optional[Any]:
    """
    Get value from cache (Redis or memory).
    
    Args:
        key: Cache key
        
    Returns:
        Cached value or None if not found
    """
    # Try Redis first
    if is_redis_available():
        try:
            redis_client = get_redis_client()
            if redis_client:
                cached = redis_client.get(key)
                if cached:
                    return json.loads(cached)
        except Exception as e:
            logger.warning(f"Redis get error: {str(e)}, falling back to memory cache")
    
    # Fallback to memory cache
    if key in _memory_cache:
        ttl = _memory_cache_ttl.get(key, 0)
        if ttl > time.time():
            return _memory_cache[key]
        else:
            # Expired, remove it
            _memory_cache.pop(key, None)
            _memory_cache_ttl.pop(key, None)
    
    return None


def set_in_cache(key: str, value: Any, ttl: Optional[int] = None) -> bool:
    """
    Set value in cache (Redis or memory).
    
    Args:
        key: Cache key
        value: Value to cache (must be JSON serializable)
        ttl: Time to live in seconds (defaults to settings.cache_ttl_seconds)
        
    Returns:
        True if successful, False otherwise
    """
    if ttl is None:
        ttl = settings.cache_ttl_seconds
    
    try:
        # Try Redis first
        if is_redis_available():
            try:
                redis_client = get_redis_client()
                if redis_client:
                    json_value = json.dumps(value)
                    redis_client.setex(key, ttl, json_value)
                    return True
            except Exception as e:
                logger.warning(f"Redis set error: {str(e)}, falling back to memory cache")
        
        # Fallback to memory cache
        _memory_cache[key] = value
        _memory_cache_ttl[key] = time.time() + ttl
        return True
    except Exception as e:
        logger.error(f"Cache set error: {str(e)}")
        return False


def delete_from_cache(key: str) -> bool:
    """
    Delete value from cache.
    
    Args:
        key: Cache key
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Try Redis first
        if is_redis_available():
            try:
                redis_client = get_redis_client()
                if redis_client:
                    redis_client.delete(key)
            except Exception as e:
                logger.warning(f"Redis delete error: {str(e)}")
        
        # Also remove from memory cache
        _memory_cache.pop(key, None)
        _memory_cache_ttl.pop(key, None)
        return True
    except Exception as e:
        logger.error(f"Cache delete error: {str(e)}")
        return False


def invalidate_pattern(pattern: str) -> int:
    """
    Invalidate all cache keys matching a pattern.
    
    Args:
        pattern: Pattern to match (supports * wildcard)
        
    Returns:
        Number of keys invalidated
    """
    count = 0
    
    # Try Redis first
    if is_redis_available():
        try:
            redis_client = get_redis_client()
            if redis_client:
                # Convert pattern to Redis pattern
                redis_pattern = pattern.replace("*", "*")
                keys = redis_client.keys(redis_pattern)
                if keys:
                    redis_client.delete(*keys)
                    count = len(keys)
        except Exception as e:
            logger.warning(f"Redis pattern delete error: {str(e)}")
    
    # Also check memory cache (simple pattern matching)
    if "*" in pattern:
        # Simple wildcard matching: replace * with empty string and check if pattern is in key
        pattern_base = pattern.replace("*", "")
        memory_keys = [k for k in _memory_cache.keys() if pattern_base in k]
    else:
        # Exact match
        memory_keys = [k for k in _memory_cache.keys() if k == pattern]
    for key in memory_keys:
        _memory_cache.pop(key, None)
        _memory_cache_ttl.pop(key, None)
        count += 1
    
    return count


def cached(prefix: str, ttl: Optional[int] = None):
    """
    Decorator to cache function results.
    
    Args:
        prefix: Cache key prefix
        ttl: Time to live in seconds
        
    Example:
        @cached("animals", ttl=3600)
        def get_animals(criteria):
            ...
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            cache_key = _generate_cache_key(prefix, *args, **kwargs)
            
            # Try to get from cache
            cached_value = get_from_cache(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Store in cache
            set_in_cache(cache_key, result, ttl)
            
            return result
        
        return wrapper
    return decorator

