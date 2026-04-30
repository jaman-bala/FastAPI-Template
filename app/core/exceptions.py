from typing import Any


class BaseAppException(Exception):
    """
    Базовое исключение приложения.
    Не зависит от FastAPI, чтобы его можно было использовать в домене и сервисах.
    """

    def __init__(
        self, message: str, status_code: int = 400, headers: dict[str, Any] = None
    ):
        self.message = message
        self.status_code = status_code
        self.headers = headers
        super().__init__(message)


class AuthException(BaseAppException):
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message, status_code=401, headers={"WWW-Authenticate": "Bearer"}
        )


class InvalidTokenException(AuthException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message=message)


class ExpiredTokenException(AuthException):
    def __init__(self, message: str = "Token has expired"):
        super().__init__(message=message)


class TokenValidationException(AuthException):
    def __init__(self, message: str = "Token validation failed"):
        super().__init__(message=message)


class UserNotActiveException(AuthException):
    def __init__(self, message: str = "User is inactive"):
        super().__init__(message=message)


class ForbiddenException(BaseAppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message=message, status_code=403)
