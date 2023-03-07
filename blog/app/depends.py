from db import blog_collection
from repositories import BlogRepository

import datetime


async def get_blog_repository() -> BlogRepository:
    return BlogRepository(blog_collection)

async def get_current_time() -> datetime.datetime:
    return datetime.datetime.now().replace(microsecond=0)
