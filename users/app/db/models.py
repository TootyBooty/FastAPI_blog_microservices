from typing import Optional

from sqlmodel import SQLModel, Field

from pydantic import EmailStr
from uuid import UUID

class User(SQLModel, table=True):
    __tablename__ = 'users'

    user_id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: EmailStr = Field(unique=True)
    password: str
    is_active: bool = Field(default=True)
    # TODO
    # roles 

class UserCreate(SQLModel):
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: EmailStr = Field(unique=True)
    password: str
