from fastapi import APIRouter, Body, Depends
from sqlalchemy.exc import IntegrityError

from uuid6 import UUID

from db.repositories import UserRepository
from api.depends import get_user_repository
from api.schemas import UserCreate, UserUpdate, UserOut, UserShow
import exceptions as exc


user_router = APIRouter()



@user_router.get('/', response_model=UserShow)
async def get_user_by_id(
    user_id:UUID,
    repo:UserRepository = Depends(get_user_repository)
    ):
    user = await repo.get_user_by_id(user_id)
    if user is None:
        raise exc.InvalidUserId
    return user


@user_router.post('/', response_model=UserOut)
async def create_user(
    user_data:UserCreate = Body(),
    repo:UserRepository = Depends(get_user_repository)
    ):
    try:
        return  await repo.create_user(user_data)
    except IntegrityError:
        raise exc.EmailAlreadyTaken


@user_router.patch('/', response_model=UserOut)
async def update_user_by_id(
    user_id:UUID,
    body:UserUpdate,
    repo:UserRepository = Depends(get_user_repository)
   ):
    update_data = body.dict(exclude_none=True)
    if update_data == {}:
        raise exc.EmptyUpdatedData
    
    try:
        updated_user_id =  await repo.update_user(user_id, update_data)
    except IntegrityError as err:
        raise exc.EmailAlreadyTaken
    
    if updated_user_id is None:
        raise exc.InvalidUserId
    return UserOut(user_id=updated_user_id)


@user_router.delete('/', response_model=UserOut)
async def delete_user(
    user_id:UUID,
    repo:UserRepository = Depends(get_user_repository)
    ):
    deleted_user_id =  await repo.delete_user(user_id)
    if deleted_user_id is None:
        raise exc.InvalidUserId
    return UserOut(user_id=deleted_user_id)


# added during testing
from db.models import User
from db.session import get_session
from sqlmodel import select

@user_router.get("/all", response_model=list[UserShow])
async def get_users(session = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [UserShow(
        user_id=user.user_id, name=user.name, surname=user.surname, email=user.email, is_active=user.is_active, roles=user.roles)
          for user in users]