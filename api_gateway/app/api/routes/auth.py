from api.depends import get_aiohttp_session
from api.schemas.auth import Token
from api.schemas.user import UserOutForLogin
from api.urls import user_auth_url
from core.security import create_access_token
from fastapi import APIRouter
from fastapi import Depends
from fastapi.security import OAuth2PasswordRequestForm
from network import make_request


auth_router = APIRouter()


@auth_router.post("/token")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_aiohttp_session),
):
    login_data = {"email": form_data.username, "password": form_data.password}
    response = await make_request(
        session=session, url=user_auth_url, method="post", data=login_data
    )

    user_data = UserOutForLogin(
        email=response.get("email"), roles=response.get("roles")
    )
    access_token = create_access_token(
        data={"sub": user_data.email, "roles": user_data.roles}
    )
    return Token(access_token=access_token, token_type="bearer")
