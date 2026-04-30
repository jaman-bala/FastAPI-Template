import jwt
import uuid
import logging

from datetime import datetime, timezone, timedelta

from app.core.config import settings
from app.core.exceptions import (
    InvalidTokenException,
    ExpiredTokenException,
    TokenValidationException,
)
from app.core.security.permissions import get_permissions_by_role
from app.core.security.token_store import TokenStore
from app.domain.enums import UserRole

logger = logging.getLogger(__name__)

_AUDIENCE = "backend-api"


class JWTManager:
    def __init__(self, token_store: TokenStore) -> None:
        self.algorithm = settings.JWT_ALGORITHM
        self.secret_key = settings.JWT_SECRET_KEY.get_secret_value()
        self.access_token_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        self.refresh_token_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        self._store = token_store

    def create_token_payload(
        self, user_id: str, role: UserRole, token_type: str = "access"
    ) -> dict:
        permissions = get_permissions_by_role(role)
        now = datetime.now(timezone.utc)
        expire = now + (
            self.access_token_expire if token_type == "access" else self.refresh_token_expire
        )

        return {
            "sub": user_id,
            "user_id": user_id,
            "role": role.value if isinstance(role, UserRole) else role,
            "scopes": [p.value for p in permissions],
            "token_type": token_type,
            "jti": str(uuid.uuid4()),
            "iat": now,
            "exp": expire,
            "iss": settings.PROJECT_NAME,
            "aud": _AUDIENCE,
            "version": "1.0",
        }

    async def create_token(self, payload: dict) -> str:
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
            exp: datetime = payload["exp"]
            ttl = int((exp - datetime.now(timezone.utc)).total_seconds())
            if ttl > 0:
                await self._store.store_jti(payload["jti"], payload["user_id"], ttl)
            return token
        except Exception as e:
            logger.error("Token creation failed: %s", e)
            raise InvalidTokenException("Token creation failed") from e

    async def validate_token(self, token: str, token_type: str = "access") -> dict:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=_AUDIENCE,
                issuer=settings.PROJECT_NAME,
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredTokenException()
        except jwt.InvalidTokenError as e:
            raise TokenValidationException("Invalid token") from e

        if payload.get("token_type") != token_type:
            raise TokenValidationException("Invalid token type")

        if payload.get("version") != "1.0":
            raise TokenValidationException("Unsupported token version")

        jti = payload.get("jti")
        if not jti:
            raise TokenValidationException("Token missing jti")

        if await self._store.is_blacklisted(jti):
            raise TokenValidationException("Token has been revoked")

        return payload

    async def blacklist_token(self, token: str) -> bool:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
                audience=_AUDIENCE,
                issuer=settings.PROJECT_NAME,
                options={"verify_exp": False},
            )
        except jwt.InvalidTokenError:
            return False

        jti = payload.get("jti")
        if not jti:
            return False

        exp = payload.get("exp")
        if exp:
            ttl = int(exp - datetime.now(timezone.utc).timestamp())
            if ttl > 0:
                await self._store.blacklist_jti(jti, ttl)
                return True

        return False

    async def blacklist_user_tokens(self, user_id: str) -> int:
        keys = await self._store.get_user_jti_keys(user_id)
        count = 0
        for key in keys:
            ttl = await self._store.get_key_ttl(key)
            if ttl > 0:
                jti = key.split(":")[-1]
                await self._store.blacklist_jti(jti, ttl)
                count += 1
        logger.info("Blacklisted %d tokens for user %s", count, user_id)
        return count