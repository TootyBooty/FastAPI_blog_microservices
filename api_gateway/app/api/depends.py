from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from aiohttp import ClientSession
from jose import jwt, JWTError

from core.config import Config

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
        payload = jwt.decode(
            token, Config.SECRET_KEY, algorithms=[Config.ALGORITHM]
        )
        email: str = payload.get("sub")
        roles: list = payload.get('roles')
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return {'email': email, 'roles': roles}