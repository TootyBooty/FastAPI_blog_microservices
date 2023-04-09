from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from api.depends import get_aiohttp_session
from api.urls import user_auth_url
from api.schemas.auth import Token
from api.schemas.user import UserOutForLogin

from network import make_request
from core.config import Config
from core.security import create_access_token



auth_router = APIRouter()


@auth_router.post('/token')
async def login(
    form_data:OAuth2PasswordRequestForm = Depends(),
    session = Depends(get_aiohttp_session)
    ):
    login_data = {'email': form_data.username, 'password': form_data.password}
    response = await make_request(session=session, url=user_auth_url, method='post', data=login_data)
    
    user_data = UserOutForLogin(email=response.get('email'), roles=response.get('roles'))
    access_token = create_access_token(data={'sub': user_data.email, 'roles': user_data.roles})
    return Token(access_token=access_token, token_type='bearer')