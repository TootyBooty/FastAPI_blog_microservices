from fastapi import APIRouter, Depends

from depends import get_blog_repository
from repositories import BlogRepository


blog_router = APIRouter()

@blog_router.get('/get_all/')
async def get_all(
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    return await repo.get_posts()


@blog_router.get('/add/')
async def add(
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    return await repo.add_post()

