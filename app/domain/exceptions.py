from app.core.exceptions import BaseAppException


class DomainException(BaseAppException):
    """Базовое исключение для доменного слоя (бизнес-логика)."""

    def __init__(self, message: str, status_code: int = 404):
        super().__init__(message=message, status_code=status_code)


class ObjectNotFoundException(DomainException):
    """Общее исключение, если что-то не найдено."""

    def __init__(self, message: str = "Object not found"):
        super().__init__(message=message, status_code=404)


class UserNotFoundException(ObjectNotFoundException):
    """Специфичное исключение для пользователя."""

    def __init__(self, message: str = "User not found"):
        super().__init__(message=message)


class AlreadyExistsException(DomainException):
    """Если пытаемся создать дубликат (например, телефон)."""

    def __init__(self, message: str = "Object already exists"):
        super().__init__(message=message, status_code=409)


class InvalidTokenException(DomainException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message=message, status_code=401)


class ExpiredTokenException(DomainException):
    def __init__(self, message: str = "Expired token"):
        super().__init__(message=message, status_code=401)
