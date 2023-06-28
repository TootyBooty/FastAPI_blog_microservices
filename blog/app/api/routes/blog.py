from uuid import UUID

import exceptions as exc
from api.depends import get_blog_repository
from api.depends import get_current_time
from api.schemas import CommentIn
from api.schemas import CommentOut
from api.schemas import Post
from api.schemas import PostIn
from api.schemas import PostOut
from api.schemas import PostUpdate
from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from fastapi import Path
from fastapi import Query
from pydantic import EmailStr
from repositories import BlogRepository


blog_router = APIRouter()


@blog_router.get("/post")
async def get_post_list(
    limit: int = Query(default=50, ge=1),
    repo: BlogRepository = Depends(get_blog_repository),
) -> list[Post]:
    posts = await repo.get_posts(limit)
    return posts


@blog_router.get("/post/{post_id}", response_model=Post, status_code=200)
async def get_post(
    post_id: UUID = Path(), repo: BlogRepository = Depends(get_blog_repository)
) -> Post:
    post = await repo.get_post(post_id)
    if not post:
        raise exc.PostNotFound
    return post


@blog_router.post("/post", response_model=PostOut, status_code=201)
async def create_post(
    author: EmailStr = Query(),
    post_data: PostIn = Body(),
    current_time=Depends(get_current_time),
    repo: BlogRepository = Depends(get_blog_repository),
) -> PostOut:
    post = await repo.create_post(author, post_data, current_time)
    return post


@blog_router.patch("/post", response_model=PostOut, status_code=200)
async def update_post(
    post_id: UUID,
    body: PostUpdate,
    current_time=Depends(get_current_time),
    repo: BlogRepository = Depends(get_blog_repository),
) -> PostOut:
    update_data = body.dict(exclude_none=True)
    if update_data == {}:
        raise exc.EmptyUpdateData
    updated_post = await repo.update_post(post_id, current_time, update_data)
    if not updated_post:
        raise exc.PostNotFound
    return updated_post


@blog_router.delete("/post", response_model=PostOut, status_code=200)
async def delete_post(
    post_id: UUID, repo: BlogRepository = Depends(get_blog_repository)
) -> PostOut:
    deleted_post = await repo.delete_post(post_id)
    if not deleted_post:
        raise exc.PostNotFound
    return deleted_post


@blog_router.post("/comment", response_model=CommentOut, status_code=201)
async def add_comment(
    post_id: UUID,
    author: EmailStr = Query(),
    comment_data: CommentIn = Body(),
    current_time=Depends(get_current_time),
    repo: BlogRepository = Depends(get_blog_repository),
) -> CommentOut:
    comment = await repo.add_comment(author, post_id, comment_data, current_time)
    if not comment:
        raise exc.PostNotFound
    return comment


@blog_router.delete("/comment", response_model=CommentOut, status_code=200)
async def delete_comment(
    post_id: UUID, comment_id: UUID, repo: BlogRepository = Depends(get_blog_repository)
) -> CommentOut:
    deleted_post = await repo.delete_comment(post_id, comment_id)
    if not deleted_post:
        raise exc.PostOrCommentNotFound
    return deleted_post
