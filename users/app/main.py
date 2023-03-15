from fastapi import FastAPI, APIRouter, Depends

from db.session import init_db, get_session

app = FastAPI()


# @app.on_event('startup')
# async def on_startup():
#     await init_db()

main_api_router = APIRouter(prefix='/users')

@main_api_router.get('/')
def ping():
    return {'success': True}

# test db working

from sqlalchemy.ext.asyncio import AsyncSession
from db.models import *
from sqlalchemy import select

from uuid6 import uuid6


@app.get("/get", response_model=list[User])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [User(user_id=user.user_id, name=user.name, surname=user.surname, email=user.email, password=user.password) for user in users]


@app.post("/create")
async def add_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    user = User(user_id=uuid6(), name=user.name, surname=user.surname, email=user.email, password=user.password)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

app.include_router(main_api_router)
