import redis.asyncio as redis


class RedisManager:
    def __init__(self, url: str):
        self.url = url
        self.redis: redis.Redis | None = None

    async def connect(self) -> None:
        if self.redis is None:
            self.redis = redis.from_url(self.url, encoding="utf-8", decode_responses=True)
            await self.redis.ping()

    async def close(self) -> None:
        if self.redis:
            await self.redis.aclose()
            self.redis = None
