from fastapi import Depends

from app.api.dependencies import get_current_user
from app.core.exceptions import ForbiddenException
from app.core.security.permissions import ROLE_PERMISSIONS
from app.domain.enums import Permission, UserRole
from app.domain.users import User


class PermissionChecker:
    def __init__(self, required_permissions: list[Permission]) -> None:
        self.required_permissions = required_permissions

    def __call__(self, user: User = Depends(get_current_user)) -> User:
        user_role = UserRole(user.role) if user.role else UserRole.USER
        user_permissions = ROLE_PERMISSIONS.get(user_role, set())
        for perm in self.required_permissions:
            if perm not in user_permissions:
                raise ForbiddenException(f"Permission required: {perm.value}")
        return user
