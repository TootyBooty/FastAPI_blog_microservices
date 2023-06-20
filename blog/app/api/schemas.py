import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr


class CustomModel(BaseModel):
    class Config:
        orm_mode = True


class CommentIn(CustomModel):
    content: constr(min_length=1, max_length=1000)


class Comment(CommentIn):
    author: EmailStr
    comment_id: UUID
    created_at: datetime.datetime


class CommentOut(CustomModel):
    post_id: UUID
    comment_id: UUID


class PostIn(CustomModel):
    title: constr(min_length=1, max_length=50)
    content: constr(min_length=1, max_length=5000)


class PostOut(CustomModel):
    post_id: UUID


class Post(PostIn):
    author: EmailStr
    post_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comments: list[Comment] = []


class PostUpdate(CustomModel):
    title: Optional[constr(min_length=1, max_length=50)]
    content: Optional[constr(min_length=1, max_length=5000)]
