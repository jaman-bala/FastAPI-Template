import uuid
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.user_repo import UserRepository
from app.schemas.user_schemas import LoginRequestDTO, TokenResponseDTO
from app.services.token_service import TokenService
from app.core.exceptions import AuthException, BaseAppException
from app.core.security.password_hasher import PasswordHasher
from app.domain.enums import UserRole
from app.domain.users import User


class AuthService:
    def __init__(
        self,
        session: AsyncSession,
        token_service: TokenService,
        password_hasher: PasswordHasher,
    ) -> None:
        self._repo = UserRepository(session)
        self._token_service = token_service
        self._password_hasher = password_hasher

    # ----------------- TOKEN OPERATIONS -----------------

    async def create_access_token(self, user_id: uuid.UUID, role: UserRole) -> str:
        return await self._token_service.create_token(user_id, role, "access")

    async def create_refresh_token(self, user_id: uuid.UUID, role: UserRole) -> str:
        return await self._token_service.create_token(user_id, role, "refresh")

    async def decode_access_token(self, token: str) -> dict:
        return await self._token_service.validate_token(token, "access")

    # ----------------- AUTHENTICATION -----------------

    async def login_user(self, data: LoginRequestDTO) -> TokenResponseDTO:
        user = await self._authenticate_user(data)
        role = UserRole(user.role) if user.role else UserRole.USER
        access_token = await self.create_access_token(user.id, role)
        refresh_token = await self.create_refresh_token(user.id, role)
        return TokenResponseDTO(access_token=access_token, refresh_token=refresh_token)

    async def logout(
        self,
        access_token: str | None = None,
        refresh_token: str | None = None,
        user_id: str | uuid.UUID | None = None,
    ) -> None:
        if not access_token and not refresh_token and not user_id:
            raise BaseAppException("At least one of access_token, refresh_token, or user_id must be provided")
        await self._token_service.logout_user(access_token, refresh_token, user_id)

    async def hash_password(self, password: str) -> str:
        return self._password_hasher.hash(password)

    # ----------------- PRIVATE METHODS -----------------

    async def _authenticate_user(self, data: LoginRequestDTO) -> User:
        user = await self._repo.get_by_phone(data.phone)
        if not user or not user.is_active:
            raise AuthException("Invalid credentials")
        if not self._password_hasher.verify(data.password, user.hashed_password):
            raise AuthException("Invalid credentials")
        return user


