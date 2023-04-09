from pydantic import BaseModel, EmailStr, constr

from typing import Optional
from uuid import UUID
import datetime


class CommentIn(BaseModel):
    content: constr(min_length=1, max_length=1000)

class Comment(CommentIn):
    author: EmailStr
    comment_id: UUID
    created_at: datetime.datetime
    
class CommentOut(BaseModel):
    post_id: UUID
    comment_id: UUID
 

class PostIn(BaseModel):
    title: constr(min_length=1, max_length=50)
    content: constr(min_length=1, max_length=5000)

    
class PostOut(BaseModel):
    post_id: UUID


class Post(PostIn):
    author: EmailStr
    post_id: UUID
    created_at: datetime.datetime
    updated_at: datetime.datetime
    comments: list[Comment] = []


class PostUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=50)]
    content: Optional[constr(min_length=1, max_length=5000)]
