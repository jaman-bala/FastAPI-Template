from app.core.config import settings


def validate_phone_number(value: str) -> str:
    """Простая валидация номера телефона через regex из настроек."""
    if not settings.PHONE_REGEX.match(value):
        raise ValueError("Invalid phone number format. Example: +996500500500")
    return value


def validate_email(value: str) -> str:
    """Валидация email через regex и приведение к нижнему регистру."""
    if value:
        if not settings.EMAIL_REGEX.match(value):
            raise ValueError("Некорректный формат email")
        return value.lower()
    return value


def validate_password(value: str) -> str:
    if not settings.PASSWORD_REGEX.match(value):
        raise ValueError("Invalid password format. Example: ")
    return value
