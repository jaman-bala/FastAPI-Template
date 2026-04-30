import uuid

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AuthException
from app.core.init import jwt_manager
from app.core.security.password_hasher import PasswordHasher
from app.domain.users import User
from app.infrastructure.database import get_unit_of_work
from app.repositories.user_repo import UserRepository
from app.services.auth_service import AuthService
from app.services.token_service import TokenService

_bearer = HTTPBearer()

_token_service = TokenService()
_password_hasher = PasswordHasher()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(_bearer),
    session: AsyncSession = Depends(get_unit_of_work),
) -> User:
    payload = await jwt_manager.validate_token(credentials.credentials, "access")
    user_id_str = payload.get("user_id")
    if not user_id_str:
        raise AuthException("Invalid token payload")
    user = await UserRepository(session).find_one_or_none(id=uuid.UUID(user_id_str))
    if not user or not user.is_active:
        raise AuthException("User not found or inactive")
    return user


def get_auth_service(session: AsyncSession = Depends(get_unit_of_work)) -> AuthService:
    return AuthService(session, _token_service, _password_hasher)