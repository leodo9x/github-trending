import pytest
from datetime import datetime, timedelta
from app.services.cache_service import InMemoryCache

@pytest.fixture
def cache():
    return InMemoryCache()

def test_cache_set_get(cache):
    """Test basic set and get operations."""
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

def test_cache_expiration(cache):
    """Test cache expiration."""
    cache.ttl = 1  # Set TTL to 1 second
    cache.set("test_key", "test_value")
    assert cache.get("test_key") == "test_value"

    # Simulate time passing
    cache._timestamps["test_key"] = datetime.now() - timedelta(seconds=2)
    assert cache.get("test_key") is None

def test_cache_delete(cache):
    """Test cache deletion."""
    cache.set("test_key", "test_value")
    cache.delete("test_key")
    assert cache.get("test_key") is None

def test_cache_clear_all(cache):
    """Test clearing all cache entries."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.clear_all()
    assert cache.get("key1") is None
    assert cache.get("key2") is None

def test_cache_max_size(cache):
    """Test cache size limit enforcement."""
    cache.max_size = 2
    cache.set("key1", "value1")
    cache.set("key2", "value2")
    cache.set("key3", "value3")

    # The oldest item should be removed
    assert cache.get("key1") is None
    assert cache.get("key2") is not None
    assert cache.get("key3") is not None

def test_cache_cleanup_expired(cache):
    """Test cleanup of expired items."""
    cache.set("key1", "value1")
    cache.set("key2", "value2")

    # Make key1 expired
    cache._timestamps["key1"] = datetime.now() - timedelta(seconds=1)

    # Trigger cleanup by getting a value
    cache.get("key2")

    assert cache.get("key1") is None
    assert cache.get("key2") is not None