import datetime
import uuid

from pydantic import BaseModel, ConfigDict, Field

from app.domain.enums import UserRole
from app.utils.common_types import PhoneNumber, EmailField, PasswordField


class UserBase(BaseModel):
    email: EmailField | None = Field(None, description="Email пользователя")
    phone: PhoneNumber = Field(..., description="Номер телефона (обязателен)")
    first_name: str | None = Field(None, max_length=100, description="Имя")
    last_name: str | None = Field(None, max_length=100, description="Фамилия")
    middle_name: str | None = Field(None, max_length=100, description="Отчество")
    role: UserRole = Field(default=UserRole.USER, description="Роль")
    photo: str | None = Field(None, description="Url изображении")


class UserRequestDTO(BaseModel):
    password: PasswordField = Field(
        ..., min_length=8, max_length=72, description="Пароль"
    )


class UserUpdateDTO(BaseModel):
    email: EmailField | None = Field(None, description="Email пользователя")
    phone: PhoneNumber = Field(..., description="Номер телефона (обязателен)")
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    middle_name: str | None = Field(None, max_length=100)


class UserResponseDTO(UserBase):
    id: uuid.UUID
    role: str | None
    is_active: bool
    created_at: datetime.datetime
    model_config = ConfigDict(from_attributes=True)

class LoginRequestDTO(BaseModel):
    phone: PhoneNumber
    password: PasswordField

class TokenResponseDTO(BaseModel):
    access_token: str
    refresh_token: str
    model_config = ConfigDict(from_attributes=True)
