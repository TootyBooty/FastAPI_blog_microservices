from uuid import UUID

from aiohttp import ClientSession
from api.schemas.user import UserOutForLogin
from api.schemas.user import UserShow
from api.urls import user_base_url
from api.urls import user_profile_url
from core.config import Config
from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from network import make_request
from pydantic import EmailStr

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/token")


async def get_aiohttp_session() -> ClientSession:
    """Dependency for getting aiohttp session"""
    try:
        session = ClientSession()
        yield session
    finally:
        await session.close()


async def get_user_data_from_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM])
        email: str = payload.get("sub")
        roles: list = payload.get("roles")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return UserOutForLogin(email=email, roles=roles)


async def get_target_user_by_id(
    user_id: UUID,
) -> UserShow:
    session = ClientSession()
    user = await make_request(
        session=session,
        url=user_base_url,
        method="get",
        params={"user_id": user_id.hex},
    )
    return UserShow(**user)


async def get_target_user_by_email(
    author: EmailStr,
) -> UserShow:
    session = ClientSession()
    user = await make_request(
        session=session, url=user_profile_url, method="get", params={"email": author}
    )
    return UserShow(**user)
