from app.core.config import settings
from app.infrastructure.redis import RedisManager
from app.infrastructure.redis_token_store import RedisTokenStore
from app.core.security.jwt_manager import JWTManager

redis_manager = RedisManager(url=settings.REDIS_URL)
_token_store = RedisTokenStore(redis_manager)
jwt_manager = JWTManager(_token_store)