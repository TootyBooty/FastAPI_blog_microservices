from fastapi import Depends

from db.session import get_session
from db.repositories import UserRepository

async def get_user_repository(session = Depends(get_session)) -> UserRepository:
    return UserRepository(session)


