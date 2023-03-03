from db import blog_collection
from repositories import BlogRepository


async def get_blog_repository() -> BlogRepository:
    return BlogRepository(blog_collection)
