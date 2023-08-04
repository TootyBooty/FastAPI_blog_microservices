from uuid import UUID

from api.depends import get_aiohttp_session
from api.depends import get_target_user_by_id
from api.depends import get_user_data_from_token
from api.schemas.user import UserCreate
from api.schemas.user import UserOut
from api.schemas.user import UserRole
from api.schemas.user import UserShow
from api.schemas.user import UserUpdate
from api.schemas.user import UserUpdateRole
from api.urls import user_base_url
from api.urls import user_list_url
from api.urls import user_ping_url
from api.urls import user_role_url
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from network import make_request
from permissions import check_permissions
from permissions import PermissionDenied


user_router = APIRouter()


@user_router.get("/ping")
async def ping_user(session=Depends(get_aiohttp_session)):
    return await make_request(session=session, url=user_ping_url, method="get")


@user_router.get("/", response_model=list[UserShow])
async def get_user_list(
    limit: int = Query(ge=1, default=50),
    offset: int = Query(ge=0, default=0),
    session=Depends(get_aiohttp_session),
):
    return await make_request(
        session=session,
        url=user_list_url,
        method="get",
        params={"limit": limit, "offset": offset},
    )


@user_router.get("/{user_id}/", response_model=UserShow)
async def get_user_by_id(user_id: UUID = Path(), session=Depends(get_aiohttp_session)):
    return await make_request(
        session=session, url=f"{user_base_url}{user_id}/", method="get"
    )


@user_router.post("/", response_model=UserShow)
async def create_user(
    user_data: UserCreate = Body(), session=Depends(get_aiohttp_session)
):
    return await make_request(
        session=session, url=user_base_url, method="post", data=user_data.dict()
    )


@user_router.patch("/", response_model=UserOut)
async def update_user_by_id(
    body: UserUpdate,
    current_user=Depends(get_user_data_from_token),
    target_user=Depends(get_target_user_by_id),
    session=Depends(get_aiohttp_session),
):
    if not check_permissions(
        allowed_roles={UserRole.ROLE_ADMIN},
        current_user=current_user,
        target_user=target_user,
    ):
        raise PermissionDenied
    return await make_request(
        session=session,
        url=user_base_url,
        method="patch",
        data=body.dict(exclude_none=True),
        params={"user_id": target_user.user_id.hex},
    )


@user_router.delete("/", response_model=UserOut)
async def delete_user(
    current_user=Depends(get_user_data_from_token),
    target_user=Depends(get_target_user_by_id),
    session=Depends(get_aiohttp_session),
):
    if not check_permissions(
        allowed_roles={UserRole.ROLE_ADMIN},
        current_user=current_user,
        target_user=target_user,
    ):
        raise PermissionDenied
    return await make_request(
        session=session,
        url=user_base_url,
        method="delete",
        params={"user_id": target_user.user_id.hex},
    )


@user_router.post("/role", response_model=UserOut)
async def add_role(
    role_to_change: UserUpdateRole = Body(),
    current_user=Depends(get_user_data_from_token),
    target_user=Depends(get_target_user_by_id),
    session=Depends(get_aiohttp_session),
):
    if not check_permissions(
        allowed_roles={UserRole.ROLE_ADMIN},
        current_user=current_user,
        target_user=target_user,
    ):
        raise PermissionDenied
    return await make_request(
        session=session,
        url=user_role_url,
        method="post",
        data={"role": role_to_change.role.value},
        params={"user_id": target_user.user_id.hex},
    )


@user_router.delete("/role", response_model=UserOut)
async def delete_role(
    role_to_change: UserUpdateRole = Body(),
    current_user=Depends(get_user_data_from_token),
    target_user=Depends(get_target_user_by_id),
    session=Depends(get_aiohttp_session),
):
    if not check_permissions(
        allowed_roles={UserRole.ROLE_ADMIN},
        current_user=current_user,
        target_user=target_user,
    ):
        raise PermissionDenied
    return await make_request(
        session=session,
        url=user_role_url,
        method="delete",
        data={"role": role_to_change.role.value},
        params={"user_id": target_user.user_id.hex},
    )
