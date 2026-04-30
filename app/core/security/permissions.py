from app.domain.enums import UserRole, Permission

# Маппинг ролей к их разрешениям
ROLE_PERMISSIONS: dict[UserRole, set[Permission]] = {
    UserRole.USER: {
        Permission.ITEMS_CREATE,
    },
    UserRole.ADMIN: {
        Permission.USERS_VIEW,
        Permission.ITEMS_CREATE,
        Permission.ITEMS_EDIT,
        Permission.ITEMS_DELETE,
    },
    UserRole.SUPERUSER: set(Permission),  # Все права
}


def get_permissions_by_role(role: UserRole) -> set[Permission]:
    return ROLE_PERMISSIONS.get(role, set())
