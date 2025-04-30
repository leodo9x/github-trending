from typing import Any, Optional
from datetime import datetime, timedelta
from ..config.settings import settings

class InMemoryCache:
    def __init__(self):
        self._cache = {}
        self._timestamps = {}
        self.max_size = settings.CACHE_MAX_SIZE
        self.ttl = settings.CACHE_TTL

    def _is_expired(self, key: str) -> bool:
        if key not in self._timestamps:
            return True
        return datetime.now() > self._timestamps[key]

    def _cleanup_expired(self):
        """Remove expired items from cache."""
        expired_keys = [k for k in self._cache.keys() if self._is_expired(k)]
        for key in expired_keys:
            del self._cache[key]
            del self._timestamps[key]

    def _enforce_max_size(self):
        """Remove oldest items if cache exceeds max size."""
        if len(self._cache) > self.max_size:
            # Sort by timestamp and remove oldest items
            sorted_items = sorted(self._timestamps.items(), key=lambda x: x[1])
            items_to_remove = len(self._cache) - self.max_size
            for key, _ in sorted_items[:items_to_remove]:
                del self._cache[key]
                del self._timestamps[key]

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache if it exists and is not expired."""
        self._cleanup_expired()
        if key in self._cache and not self._is_expired(key):
            return self._cache[key]
        return None

    def set(self, key: str, value: Any) -> None:
        """Set value in cache with expiration."""
        self._cleanup_expired()
        self._cache[key] = value
        self._timestamps[key] = datetime.now() + timedelta(seconds=self.ttl)
        self._enforce_max_size()

    def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self._cache:
            del self._cache[key]
            del self._timestamps[key]

    def clear_all(self) -> None:
        """Clear all cache entries."""
        self._cache.clear()
        self._timestamps.clear()

# Create a singleton instance
cache = InMemoryCache()