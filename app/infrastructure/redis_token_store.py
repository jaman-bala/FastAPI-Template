from app.infrastructure.redis import RedisManager


class RedisTokenStore:
    _JTI_KEY = "token_jti:{user_id}:{jti}"
    _BLACKLIST_KEY = "blacklist:{jti}"

    def __init__(self, redis_manager: RedisManager) -> None:
        self._manager = redis_manager

    @property
    def _redis(self):
        return self._manager.redis

    async def store_jti(self, jti: str, user_id: str, ttl: int) -> None:
        key = self._JTI_KEY.format(user_id=user_id, jti=jti)
        await self._redis.set(key, "1", ex=ttl)

    async def is_blacklisted(self, jti: str) -> bool:
        return await self._redis.exists(self._BLACKLIST_KEY.format(jti=jti)) > 0

    async def blacklist_jti(self, jti: str, ttl: int) -> None:
        await self._redis.set(self._BLACKLIST_KEY.format(jti=jti), "1", ex=ttl)

    async def get_user_jti_keys(self, user_id: str) -> list[str]:
        pattern = self._JTI_KEY.format(user_id=user_id, jti="*")
        return [key async for key in self._redis.scan_iter(pattern)]

    async def get_key_ttl(self, key: str) -> int:
        return await self._redis.ttl(key)