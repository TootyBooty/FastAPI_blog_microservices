from fastapi import Header, Body, HTTPException

from config import Config
from db import blog_collection
from repositories import BlogRepository

from typing import Annotated
import datetime


async def get_blog_repository() -> BlogRepository:
    return BlogRepository(blog_collection)


async def get_current_time() -> datetime.datetime:
    return datetime.datetime.now().replace(microsecond=0)


async def verify_token(api_gateway_token = Header()):
    if api_gateway_token != Config.API_GATEWAY_TOKEN:
        raise HTTPException(status_code=400, detail="Wrong sender.")
    
async def get_authorized_user(authorized_user = Body()):
    if not authorized_user:
        raise HTTPException(status_code=400, detail='user not authorized.')
    user_data = authorized_user.get('authorized_user')
    return {'email': user_data.get('email'), 'roles': user_data.get('roles')}