from pydantic import BaseModel, Field, EmailStr, constr

import enum
from typing import Optional
from uuid import UUID


class UserRole(str, enum.Enum):
    ROLE_USER = "USER"
    ROLE_MODERATOR = "MODERATOR"
    ROLE_ADMIN = "ADMIN"
    ROLE_SUPERADMIN = "SUPERADMIN"


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
    roles: list[UserRole]


class UserOut(CustomModel):
    user_id: UUID


class UserOutForLogin(CustomModel):
    email: EmailStr
    roles: list[UserRole]