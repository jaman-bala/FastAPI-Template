from enum import Enum


class UserRole(str, Enum):
    SUPERUSER = "superuser"
    ADMIN = "admin"
    USER = "user"


class Permission(str, Enum):
    USERS_VIEW = "users:view"
    USERS_EDIT = "users:edit"
    USERS_DELETE = "users:delete"

    # Права для контента (например, книг или постов)
    ITEMS_CREATE = "items:create"
    ITEMS_EDIT = "items:edit"
    ITEMS_DELETE = "items:delete"
