from fastapi import APIRouter, Depends, Body

from network import make_request

from api.depends import get_aiohttp_session, get_user_data_from_token
from api.schemas.user import UserShow, UserOut, UserUpdate, UserCreate
from api.urls import user_base_url
from uuid import UUID


user_router = APIRouter()


@user_router.get('/', response_model=UserShow)
async def get_user_by_id(
    user_id:UUID,
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=user_base_url, method='get', params={'user_id': user_id.hex})


@user_router.post('/', response_model=UserOut)
async def create_user(
    user_data:UserCreate = Body(),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=user_base_url, method='post', data=user_data.dict())
    

@user_router.patch('/', response_model=UserOut)
async def update_user_by_id(
    user_id:UUID,
    body:UserUpdate,
    session = Depends(get_aiohttp_session)
   ):
    return await make_request(session=session, url=user_base_url, method='patch', data=body.dict(exclude_none=True), params={'user_id': user_id.hex})


@user_router.delete('/', response_model=UserOut)
async def delete_user(
    user_id:UUID,
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=user_base_url, method='delete', params={'user_id': user_id.hex})


@user_router.get('/test')
async def test_user(
    authorized_user = Depends(get_user_data_from_token),
                    session = Depends(get_aiohttp_session)):
    return await make_request(session=session, url=f'{user_base_url}/test_user', method='get', authorized_user=authorized_user)