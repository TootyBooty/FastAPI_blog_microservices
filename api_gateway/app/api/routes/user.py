from fastapi import APIRouter, Depends, Body, Query

from network import make_request
from permissions import check_permissions, PermissionDenied

from api.depends import get_aiohttp_session, get_user_data_from_token, get_target_user_by_id
from api.schemas.user import UserShow, UserOut, UserUpdate, UserCreate, UserRole, UserUpdateRole
from api.urls import user_base_url, user_all_url, user_role_url



user_router = APIRouter()


@user_router.get("/all", response_model=list[UserShow])
async def get_all_users(
    limit: int = Query(ge=1, default=50),
    offset: int = Query(ge=0, default=0),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=user_all_url, method='get',
                               params={'limit': limit, 'offset': offset})


@user_router.get('/', response_model=UserShow)
async def get_user_by_id(
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_id)
    ):
    return target_user


@user_router.post('/', response_model=UserShow)
async def create_user(
    user_data:UserCreate = Body(),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=user_base_url, method='post',
                               data=user_data.dict())
    

@user_router.patch('/', response_model=UserOut)
async def update_user_by_id(
    body:UserUpdate,
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_id),
    session = Depends(get_aiohttp_session)
   ):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=user_base_url, method='patch',
                               data=body.dict(exclude_none=True), params={'user_id': target_user.user_id.hex})


@user_router.delete('/', response_model=UserOut)
async def delete_user(
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_id),
    session = Depends(get_aiohttp_session)
    ):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=user_base_url, method='delete',
                               params={'user_id': target_user.user_id.hex})


@user_router.post('/role', response_model=UserOut)
async def add_role(
    role_to_change: UserUpdateRole = Body(),
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_id),
    session = Depends(get_aiohttp_session)
):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=user_role_url, method='post',
                               data={'role': role_to_change.role.value}, params={'user_id': target_user.user_id.hex})


@user_router.delete('/role', response_model=UserOut)
async def delete_role(
    role_to_change: UserUpdateRole = Body(),
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_id),
    session = Depends(get_aiohttp_session)
):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=user_role_url, method='delete',
                               data={'role': role_to_change.role.value}, params={'user_id': target_user.user_id.hex})