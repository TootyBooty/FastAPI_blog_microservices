from fastapi import APIRouter, HTTPException, Depends, Body, Query
from fastapi.responses import JSONResponse

from uuid import UUID

from depends import get_blog_repository, get_current_time
from repositories import BlogRepository
from schemas import Post, PostIn, PostUpdate, PostOut, CommentIn


blog_router = APIRouter()


@blog_router.get('/get_all/')
async def get_all(
    limit:int = Query(default=None, ge=1),
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    return await repo.get_posts(limit)


@blog_router.get('/post/', response_model=Post, status_code=200)
async def get_post(
    post_id:UUID = Query(),
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    res = await repo.get_post(post_id)
    if not res:
        raise HTTPException(404, 'post not found.')
    return res


@blog_router.post('/post/', response_model=PostOut, status_code=201)
async def create_post(
    post_data:PostIn = Body(),
    current_time = Depends(get_current_time),
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    return await repo.create_post(post_data, current_time)


@blog_router.patch('/post/', response_model=PostOut, status_code=200)
async def update_post(
    post_id:UUID,
    body:PostUpdate,
    current_time = Depends(get_current_time),
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    update_data = body.dict(exclude_none=True)
    if update_data == {}:
        raise HTTPException(status_code=422, detail='At least one field must be changed.')
    res = await repo.update_post(post_id, current_time,  update_data)
    if not res:
        raise HTTPException(404, 'post not found.')
    return res


@blog_router.delete('/post/', response_model=PostOut, status_code=200)
async def delete_post(
    post_id:UUID,
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    res = await repo.delete_post(post_id)
    if not res:
        raise HTTPException(404, 'post not found.')
    return res


@blog_router.post('/comment/', status_code=201)
async def add_comment(
    post_id:UUID,
    comment_data:CommentIn = Body(),
    current_time = Depends(get_current_time),
    repo:BlogRepository = Depends(get_blog_repository)    
    ):
    res = await repo.add_comment(post_id, comment_data, current_time)
    if not res:
        raise HTTPException(404, 'post not found.')
    return JSONResponse({'comment_id': str(res)})


@blog_router.delete('/comment/', status_code=200)
async def delete_comment(
    post_id:UUID,
    comment_id:UUID,
    repo:BlogRepository = Depends(get_blog_repository)
    ):
    res = await repo.delete_comment(post_id, comment_id)
    if not res:
        raise HTTPException(404, 'post or comment not found.')
    return JSONResponse({'status': 'successfully', 'detail': 'comment deleted'})