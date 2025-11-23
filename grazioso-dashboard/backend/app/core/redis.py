"""
Redis connection manager.
"""
import redis
import logging
from typing import Optional
from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: Optional[redis.Redis] = None


def get_redis_client() -> Optional[redis.Redis]:
    """
    Get Redis client instance.
    
    Returns:
        Redis client or None if Redis is disabled or unavailable
    """
    global _redis_client
    
    if not settings.redis_enabled:
        logger.debug("Redis is disabled in configuration")
        return None
    
    if _redis_client is None:
        try:
            _redis_client = redis.Redis(
                host=settings.redis_host,
                port=settings.redis_port,
                password=settings.redis_password,
                db=settings.redis_db,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            _redis_client.ping()
            logger.info("Redis connection established")
        except Exception as e:
            logger.warning(f"Failed to connect to Redis: {str(e)}. Falling back to in-memory cache.")
            _redis_client = None
    
    return _redis_client


def is_redis_available() -> bool:
    """
    Check if Redis is available.
    
    Returns:
        True if Redis is available, False otherwise
    """
    client = get_redis_client()
    if client is None:
        return False
    try:
        client.ping()
        return True
    except Exception:
        return False


def close_redis_connection():
    """Close Redis connection."""
    global _redis_client
    if _redis_client:
        try:
            _redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing Redis connection: {str(e)}")
        finally:
            _redis_client = None

