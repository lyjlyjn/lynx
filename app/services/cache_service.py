"""Cache service for file metadata and content."""
import logging
from typing import Optional, Any
import asyncio
from datetime import datetime, timedelta
import json

from app.core.config import settings

logger = logging.getLogger(__name__)


class CacheService:
    """Simple in-memory cache service."""
    
    def __init__(self):
        self.cache = {}
        self.timestamps = {}
        self.enabled = settings.cache_enabled
        self.ttl = settings.cache_ttl
        self.max_size = settings.cache_max_size
        
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.enabled:
            return None
        
        if key not in self.cache:
            return None
        
        # Check if expired
        timestamp = self.timestamps.get(key)
        if timestamp and (datetime.utcnow() - timestamp).total_seconds() > self.ttl:
            await self.delete(key)
            return None
        
        return self.cache[key]
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache."""
        if not self.enabled:
            return
        
        # Check cache size
        if len(self.cache) >= self.max_size:
            await self._evict_oldest()
        
        self.cache[key] = value
        self.timestamps[key] = datetime.utcnow()
        
        # Set custom TTL if provided
        if ttl:
            asyncio.create_task(self._expire_key(key, ttl))
    
    async def delete(self, key: str) -> None:
        """Delete value from cache."""
        if key in self.cache:
            del self.cache[key]
        if key in self.timestamps:
            del self.timestamps[key]
    
    async def clear(self) -> None:
        """Clear all cache."""
        self.cache.clear()
        self.timestamps.clear()
    
    async def _evict_oldest(self) -> None:
        """Evict oldest cache entry."""
        if not self.timestamps:
            return
        
        oldest_key = min(self.timestamps.items(), key=lambda x: x[1])[0]
        await self.delete(oldest_key)
    
    async def _expire_key(self, key: str, ttl: int) -> None:
        """Expire key after TTL seconds."""
        await asyncio.sleep(ttl)
        await self.delete(key)
    
    def get_stats(self) -> dict:
        """Get cache statistics."""
        return {
            "enabled": self.enabled,
            "size": len(self.cache),
            "max_size": self.max_size,
            "ttl": self.ttl
        }


# Global cache service instance
cache_service = CacheService()
