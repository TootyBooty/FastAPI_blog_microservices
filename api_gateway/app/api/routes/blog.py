from fastapi import APIRouter, Depends, Body, Query, Path

from network import make_request
from permissions import check_permissions, PermissionDenied

from api.depends import get_aiohttp_session, get_target_user_by_email, get_user_data_from_token
from api.schemas.blog import Post, PostIn, PostUpdate, PostOut, CommentIn, CommentOut
from api.schemas.user import UserRole
from api.urls import blog_post_url, blog_comment_url, blog_ping_url

from uuid import UUID

blog_router = APIRouter()


@blog_router.get('/ping')
async def ping_blog(
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_ping_url, method='get')


@blog_router.get("/post", response_model=list[Post])
async def get_post_list(
    limit: int = Query(ge=1, default=50),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='get',
                               params={'limit': limit})


@blog_router.get('/post/{post_id}', response_model=Post, status_code=200)
async def get_post(
    post_id:UUID = Path(),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=f'{blog_post_url}/{post_id.hex}', method='get')


@blog_router.post('/post/', response_model=PostOut, status_code=201)
async def create_post(
    post_data:PostIn = Body(),
    current_user = Depends(get_user_data_from_token),
    session = Depends(get_aiohttp_session)
    ):
    return await make_request(session=session, url=blog_post_url, method='post',
                               data=post_data.dict(), params={'author': current_user.email})


@blog_router.patch('/post/', response_model=PostOut, status_code=200)
async def update_post(
    post_id:UUID,
    body:PostUpdate,
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_email),
    session = Depends(get_aiohttp_session)
   ):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN, UserRole.ROLE_MODERATOR},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=blog_post_url, method='patch',
                               data=body.dict(exclude_none=True), params={'post_id': post_id.hex})


@blog_router.delete('/post/', response_model=PostOut, status_code=200)
async def delete_post(
    post_id:UUID,
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_email),
    session = Depends(get_aiohttp_session)
   ):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN, UserRole.ROLE_MODERATOR},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=blog_post_url, method='delete',
                               params={'post_id': post_id.hex})


@blog_router.post('/comment/', response_model=CommentOut, status_code=201)
async def add_comment(
    post_id:UUID,
    comment_data:CommentIn = Body(),
    current_user = Depends(get_user_data_from_token),
    session = Depends(get_aiohttp_session)  
    ):
    return await make_request(session=session, url=blog_comment_url, method='post',
                               data=comment_data.dict(), params={'post_id': post_id.hex, 'author': current_user.email})


@blog_router.delete('/comment/',response_model=CommentOut, status_code=200)
async def delete_comment(
    post_id:UUID,
    comment_id:UUID,
    current_user = Depends(get_user_data_from_token),
    target_user = Depends(get_target_user_by_email),
    session = Depends(get_aiohttp_session)
   ):
    if not check_permissions(allowed_roles={UserRole.ROLE_ADMIN, UserRole.ROLE_MODERATOR},
                            current_user=current_user,
                            target_user=target_user):
        raise PermissionDenied
    return await make_request(session=session, url=blog_comment_url, method='get',
                               params={'post_id': post_id.hex, 'comment_id': comment_id.hex})
