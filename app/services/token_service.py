from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from app.core.init import jwt_manager
from app.core.exceptions import InvalidTokenException, ExpiredTokenException
from app.domain.enums import UserRole

if TYPE_CHECKING:
    from app.repositories.user_repo import UserRepository


class TokenService:
    async def create_token(
        self, user_id: uuid.UUID, role: UserRole, token_type: str
    ) -> str:
        payload = jwt_manager.create_token_payload(
            user_id=str(user_id), role=role, token_type=token_type
        )
        return await jwt_manager.create_token(payload)

    async def validate_token(self, token: str, token_type: str) -> dict:
        return await jwt_manager.validate_token(token, token_type)

    async def refresh_access_token(self, refresh_token: str, user_repo: "UserRepository") -> str:
        try:
            payload = await jwt_manager.validate_token(refresh_token, "refresh")
        except (InvalidTokenException, ExpiredTokenException):
            raise InvalidTokenException("Refresh token is invalid or expired")

        user_id = uuid.UUID(payload["user_id"])
        user = await user_repo.find_one_or_none(id=user_id)
        if not user:
            raise InvalidTokenException("User not found")

        role = UserRole(user.role)
        return await self.create_token(user_id, role, "access")

    async def logout_user(
        self,
        access_token: str | None = None,
        refresh_token: str | None = None,
        user_id: str | None = None,
    ) -> None:
        if access_token:
            await jwt_manager.blacklist_token(access_token)
        if refresh_token:
            await jwt_manager.blacklist_token(refresh_token)
        if user_id:
            await jwt_manager.blacklist_user_tokens(str(user_id))