from pydantic import BaseModel, Field, EmailStr, constr

from typing import Optional
from uuid import UUID


class CustomModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(CustomModel):
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: EmailStr
    password: str


class UserUpdate(CustomModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]


class UserShow(CustomModel):
    user_id: UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    roles: list


class UserOut(CustomModel):
    user_id: UUID


class UserOutForLogin(CustomModel):
    email: EmailStr
    roles: list