from fastapi import APIRouter, HTTPException, Depends, Body, Query
from fastapi.responses import JSONResponse

from network import make_request

from api.depends import get_aiohttp_session
from api.schemas.blog import Post, PostIn, PostUpdate, PostOut, CommentIn
from uuid import UUID
from api.urls import blog_post_url, blog_comment_url

blog_router = APIRouter()




@blog_router.get('/post/', response_model=Post, status_code=200)
async def get_post(
    post_id:UUID = Query(),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='get', params={'post_id': post_id.hex})


@blog_router.post('/post/', response_model=PostOut, status_code=201)
async def create_post(
    post_data:PostIn = Body(),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='post', data=post_data.dict())


@blog_router.patch('/post/', response_model=PostOut, status_code=200)
async def update_post(
    post_id:UUID,
    body:PostUpdate,
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='patch', data=body.dict(exclude_none=True), params={'post_id': post_id.hex})


@blog_router.delete('/post/', response_model=PostOut, status_code=200)
async def delete_post(
    post_id:UUID,
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='delete', params={'post_id': post_id.hex})


@blog_router.post('/comment/', status_code=201)
async def add_comment(
    post_id:UUID,
    comment_data:CommentIn = Body(),
    session = Depends(get_aiohttp_session)  
    ):
    return await make_request(session=session, url=blog_comment_url, method='post', data=comment_data.dict(), params={'post_id': post_id.hex})


@blog_router.delete('/comment/', status_code=200)
async def delete_comment(
    post_id:UUID,
    comment_id:UUID,
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_comment_url, method='get', params={'post_id': post_id.hex, 'comment_id': comment_id.hex})
