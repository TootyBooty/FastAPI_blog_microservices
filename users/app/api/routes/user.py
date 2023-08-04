import exceptions as exc
from api.depends import get_user_repository
from api.schemas import UserCreate
from api.schemas import UserOut
from api.schemas import UserShow
from api.schemas import UserUpdate
from api.schemas import UserUpdateRole
from db.repositories import UserRepository
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from uuid6 import UUID


user_router = APIRouter()


@user_router.get("/", response_model=list[UserShow])
async def get_user_list(
    repo: UserRepository = Depends(get_user_repository),
    limit: int = Query(ge=1, default=50),
    offset: int = Query(ge=0, default=0),
):
    users = await repo.get_all_users(offset=offset, limit=limit)
    return [UserShow(**user.dict()) for user in users]


@user_router.get("/{user_id}/", response_model=UserShow)
async def get_user_by_id(
    user_id: UUID = Path(), repo: UserRepository = Depends(get_user_repository)
):
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise exc.InvalidUserId
    return user


@user_router.get("/profile", response_model=UserShow)
async def get_user_by_email(
    email: EmailStr = Query(), repo: UserRepository = Depends(get_user_repository)
):
    user = await repo.get_user_by_email(email)
    if user is None:
        raise exc.InvalidUserId
    return user


@user_router.post("/", response_model=UserShow)
async def create_user(
    user_data: UserCreate = Body(), repo: UserRepository = Depends(get_user_repository)
):
    try:
        return await repo.create_user(user_data)
    except IntegrityError:
        raise exc.EmailAlreadyTaken


@user_router.patch("/", response_model=UserOut)
async def update_user_by_id(
    body: UserUpdate,
    user_id: UUID = Query(),
    repo: UserRepository = Depends(get_user_repository),
):
    update_data = body.dict(exclude_none=True)
    if update_data == {}:
        raise exc.EmptyUpdatedData

    try:
        updated_user_id = await repo.update_user(user_id, update_data)
    except IntegrityError:
        raise exc.EmailAlreadyTaken

    if updated_user_id is None:
        raise exc.InvalidUserId
    return UserOut(user_id=updated_user_id)


@user_router.delete("/", response_model=UserOut)
async def delete_user(
    user_id: UUID = Query(), repo: UserRepository = Depends(get_user_repository)
):
    deleted_user_id = await repo.delete_user(user_id)
    if deleted_user_id is None:
        raise exc.InvalidUserId
    return UserOut(user_id=deleted_user_id)


@user_router.post("/role")
async def add_role(
    role: UserUpdateRole,
    user_id: UUID = Query(),
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise exc.InvalidUserId
    updated_roles = user.add_role_from_model(role_for_add=role.role.value)
    if updated_roles:
        await repo.update_user(user_id=user_id, update_data={"roles": updated_roles})
    return UserOut(user_id=user_id)


@user_router.delete("/role")
async def delete_role(
    role: UserUpdateRole,
    user_id: UUID = Query(),
    repo: UserRepository = Depends(get_user_repository),
):
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise exc.InvalidUserId
    updated_roles = user.remove_role_from_model(role_for_delete=role.role.value)
    if updated_roles:
        await repo.update_user(user_id=user_id, update_data={"roles": updated_roles})
    return UserOut(user_id=user_id)
