from core.config import Config
from db.repositories import UserRepository
from db.session import get_session
from fastapi import Body
from fastapi import Depends
from fastapi import Header
from fastapi import HTTPException


async def get_user_repository(session=Depends(get_session)) -> UserRepository:
    return UserRepository(session)


async def verify_token(api_gateway_token: str = Header()):
    if api_gateway_token != Config.API_GATEWAY_TOKEN:
        raise HTTPException(status_code=400, detail="Wrong sender.")


async def get_authorized_user(authorized_user=Body()):
    if not authorized_user:
        raise HTTPException(status_code=400, detail="user not authorized.")
    user_data = authorized_user.get("authorized_user")
    return {"email": user_data.get("email"), "roles": user_data.get("roles")}
