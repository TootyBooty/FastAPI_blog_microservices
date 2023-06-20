from api.schemas.user import UserOutForLogin
from api.schemas.user import UserRole
from api.schemas.user import UserShow
from fastapi import HTTPException


PermissionDenied = HTTPException(status_code=403, detail="Permission denied.")


def check_permissions(
    allowed_roles: set[UserRole],
    current_user: UserOutForLogin,
    target_user: UserShow = None,
):
    current_user_roles = set(current_user.roles)
    if target_user:
        target_user_roles = set(target_user.roles)

    # Суперадмин не может быть изменен через API
    if UserRole.ROLE_SUPERADMIN in target_user_roles:
        raise HTTPException(
            status_code=406, detail="Superadmin cannot be changed via API."
        )

    # Все остальные действия доступны суперадмину по умолчанию
    if UserRole.ROLE_SUPERADMIN in current_user_roles:
        return True

    # Если нет целевого пользователя то проверяем требуемые роли
    if not target_user_roles:
        return bool(allowed_roles & current_user_roles)

    # Пользователь может выполнять любые действия над собойе
    if current_user.email == target_user.email:
        return True

    if bool(allowed_roles & current_user_roles):
        # Админ не может быть изменен никем, кроме суперадмина
        if UserRole.ROLE_ADMIN in target_user_roles:
            return False

        # Модератор может быть изменен админом или суперадмином
        if (UserRole.ROLE_MODERATOR in target_user_roles) and (
            UserRole.ROLE_ADMIN not in current_user_roles
        ):
            return False

        # Если имеется необходимая роль и не изменяется пользователь с ролью выше, то доступ разрешен
        return True

    # Если необходимая роль отсуствует, до доступ запрещен
    return False
