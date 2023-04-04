from pydantic import BaseModel, EmailStr, constr

from typing import Optional
from uuid import UUID
import datetime


class CommentIn(BaseModel):
    creator: EmailStr
    content: constr(min_length=1, max_length=1000)

class Comment(CommentIn):
    comment_id: UUID
    created_at: datetime.datetime
 

class PostIn(BaseModel):
    creator: EmailStr
    title: constr(min_length=1, max_length=50)
    content: constr(min_length=1, max_length=5000)

    
class PostOut(PostIn):
    post_id: UUID


class Post(PostOut):
    comments: list[Comment] = []
    created_at: datetime.datetime
    updated_at: datetime.datetime

class PostUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=50)]
    content: Optional[constr(min_length=1, max_length=5000)]
