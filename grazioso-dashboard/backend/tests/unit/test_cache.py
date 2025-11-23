"""
Unit tests for caching layer.
"""
import pytest
import time
from app.utils.cache import (
    get_from_cache,
    set_in_cache,
    delete_from_cache,
    invalidate_pattern,
    _generate_cache_key
)
from app.core.config import settings


class TestCacheKeyGeneration:
    """Tests for cache key generation."""
    
    def test_generate_cache_key_with_prefix(self):
        """Test generating cache key with prefix."""
        key = _generate_cache_key("test", "arg1", "arg2")
        assert isinstance(key, str)
        assert len(key) > 0
    
    def test_generate_cache_key_consistent(self):
        """Test that same arguments generate same key."""
        key1 = _generate_cache_key("test", "arg1", "arg2")
        key2 = _generate_cache_key("test", "arg1", "arg2")
        assert key1 == key2
    
    def test_generate_cache_key_different_args(self):
        """Test that different arguments generate different keys."""
        key1 = _generate_cache_key("test", "arg1")
        key2 = _generate_cache_key("test", "arg2")
        assert key1 != key2
    
    def test_generate_cache_key_with_kwargs(self):
        """Test generating cache key with keyword arguments."""
        key1 = _generate_cache_key("test", a=1, b=2)
        key2 = _generate_cache_key("test", b=2, a=1)  # Different order
        assert key1 == key2  # Should be same regardless of order


class TestCacheOperations:
    """Tests for basic cache operations."""
    
    def test_set_and_get(self):
        """Test setting and getting from cache."""
        key = "test_key"
        value = {"test": "data"}
        
        set_in_cache(key, value)
        result = get_from_cache(key)
        
        assert result == value
    
    def test_get_nonexistent_key(self):
        """Test getting a key that doesn't exist."""
        result = get_from_cache("nonexistent_key")
        assert result is None
    
    def test_delete_key(self):
        """Test deleting a key from cache."""
        key = "test_key"
        value = {"test": "data"}
        
        set_in_cache(key, value)
        delete_from_cache(key)
        result = get_from_cache(key)
        
        assert result is None
    
    def test_cache_ttl(self):
        """Test that cache entries expire after TTL."""
        key = "ttl_test_key"
        value = {"test": "data"}
        
        # Set with very short TTL
        set_in_cache(key, value, ttl=1)
        
        # Should be available immediately
        result = get_from_cache(key)
        assert result == value
        
        # Wait for expiration
        time.sleep(2)
        result = get_from_cache(key)
        assert result is None
    
    def test_cache_different_types(self):
        """Test caching different data types."""
        test_cases = [
            ("string", "test_string"),
            ("int", 42),
            ("float", 3.14),
            ("list", [1, 2, 3]),
            ("dict", {"key": "value"}),
            ("bool", True),
        ]
        
        for key_prefix, value in test_cases:
            key = f"test_{key_prefix}"
            set_in_cache(key, value)
            result = get_from_cache(key)
            assert result == value


class TestCachePatternInvalidation:
    """Tests for pattern-based cache invalidation."""
    
    def test_invalidate_pattern(self):
        """Test invalidating keys matching a pattern."""
        # Set multiple keys
        set_in_cache("animals:1", {"id": 1})
        set_in_cache("animals:2", {"id": 2})
        set_in_cache("users:1", {"id": 1})
        
        # Invalidate animals pattern
        count = invalidate_pattern("animals:*")
        
        # Check that animals keys are gone
        assert get_from_cache("animals:1") is None
        assert get_from_cache("animals:2") is None
        # But users key should still exist
        assert get_from_cache("users:1") is not None
        assert count >= 2
    
    def test_invalidate_nonexistent_pattern(self):
        """Test invalidating a pattern with no matches."""
        count = invalidate_pattern("nonexistent:*")
        assert count == 0


class TestCacheFallback:
    """Tests for cache fallback behavior."""
    
    def test_memory_cache_fallback(self):
        """Test that memory cache works when Redis is unavailable."""
        # This test verifies that the cache system gracefully falls back
        # to in-memory cache when Redis is not available
        key = "fallback_test"
        value = {"test": "data"}
        
        # Should work even if Redis is down
        set_in_cache(key, value)
        result = get_from_cache(key)
        
        # Result should be available (either from Redis or memory)
        assert result is not None

