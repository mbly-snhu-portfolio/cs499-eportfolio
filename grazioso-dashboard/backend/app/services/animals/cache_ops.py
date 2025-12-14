"""Caching helpers for animal reads."""

from __future__ import annotations

from typing import Any, Dict, List, Optional
import logging

from app.core.config import settings
from app.utils.cache import (
    get_from_cache,
    set_in_cache,
    _generate_cache_key,
    invalidate_pattern,
)

logger = logging.getLogger(__name__)


class AnimalCacheOps:
    """Cache-aware read operations."""

    def __init__(self, reader):
        """reader must expose read(criteria, skip, limit, sort)."""
        self.reader = reader

    def read_cached(
        self,
        criteria: Optional[Dict[str, Any]] = None,
        skip: int = 0,
        limit: int = 100,
        sort: Optional[List[tuple]] = None,
    ) -> List[Dict[str, Any]]:
        cache_key = _generate_cache_key("animals:read", criteria, skip, limit, sort)

        cached_result = get_from_cache(cache_key)
        if cached_result is not None:
            logger.debug(f"Cache hit for key: {cache_key}")
            return cached_result

        result = self.reader.read(criteria, skip, limit, sort)
        set_in_cache(cache_key, result, ttl=settings.cache_ttl_seconds)
        logger.debug(f"Cache miss, stored result for key: {cache_key}")
        return result

    def invalidate_cache(self) -> None:
        try:
            patterns = ["animals:*", "trie:*"]
            for pattern in patterns:
                count = invalidate_pattern(pattern)
                if count > 0:
                    logger.info(f"Invalidated {count} cache entries matching {pattern}")
        except Exception as e:
            logger.error(f"Error invalidating cache: {str(e)}")
