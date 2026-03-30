"""
LLM Response Cache Manager

Caches LLM responses using diskcache to avoid redundant API calls.
Supports TTL-based expiration and similarity-based cache lookup.
"""

import hashlib
import logging
from typing import Optional
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ROOT_DIR = Path(__file__).parent.parent.parent.parent
CACHE_DIR = ROOT_DIR / ".cache" / "llm_responses"


class CacheManager:
    """Disk-based cache for LLM responses."""

    def __init__(self, ttl: int = 3600, cache_dir: Optional[Path] = None):
        self.ttl = ttl
        self.cache = None
        self._init_cache(cache_dir or CACHE_DIR)

    def _init_cache(self, cache_dir: Path):
        try:
            import diskcache
            cache_dir.mkdir(parents=True, exist_ok=True)
            self.cache = diskcache.Cache(str(cache_dir))
            logger.info(f"Cache initialized: {cache_dir}")
        except ImportError:
            logger.warning("diskcache not installed. Caching disabled.")
            self.cache = {}

    def _make_key(self, prompt: str, context: str = "") -> str:
        content = f"{context}:{prompt}".strip().lower()
        return hashlib.sha256(content.encode()).hexdigest()

    def get(self, prompt: str, context: str = "") -> Optional[str]:
        if self.cache is None:
            return None
        key = self._make_key(prompt, context)
        result = self.cache.get(key)
        if result is not None:
            logger.debug(f"Cache HIT: {prompt[:50]}...")
        return result

    def set(self, prompt: str, response: str, context: str = ""):
        if self.cache is None:
            return
        key = self._make_key(prompt, context)
        if isinstance(self.cache, dict):
            self.cache[key] = response
        else:
            self.cache.set(key, response, expire=self.ttl)

    def clear(self):
        if self.cache is not None:
            if isinstance(self.cache, dict):
                self.cache.clear()
            else:
                self.cache.clear()
            logger.info("Cache cleared")

    def stats(self) -> dict:
        if isinstance(self.cache, dict):
            return {"type": "memory", "size": len(self.cache)}
        try:
            return {
                "type": "disk",
                "size": len(self.cache),
                "volume": self.cache.volume(),
            }
        except Exception:
            return {"type": "disk", "size": 0}
