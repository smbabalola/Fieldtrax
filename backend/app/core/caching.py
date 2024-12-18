# app/core/caching.py
from uuid import UUID
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
import json
from typing import Any

class RedisCache:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)

    async def init(self):
        FastAPICache.init(
            RedisBackend(self.redis),
            prefix="fieldtrax-cache:"
        )

    async def set(self, key: str, value: Any, expire: int = 0):
        await self.redis.set(
            key,
            json.dumps(value),
            ex=expire if expire > 0 else None
        )

    async def get(self, key: str) -> Any:
        value = await self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def delete(self, key: str):
        await self.redis.delete(key)

    async def clear(self, pattern: str = "*"):
        async for key in self.redis.scan_iter(pattern):
            await self.redis.delete(key)

# Initialize cache
redis_cache = RedisCache("redis://localhost:6379/0")

