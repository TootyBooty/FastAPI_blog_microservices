import re
from datetime import datetime
from typing import Optional

from db.models import UserRole
from fastapi import HTTPException
from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import Field
from pydantic import validator
from uuid6 import UUID

LETTER_MATCH_PATTERN = re.compile(r"^[а-яА-Яa-zA-Z\-]+$")


class CustomModel(BaseModel):
    class Config:
        orm_mode = True


class UserCreate(CustomModel):
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: EmailStr
    password: str

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserUpdate(CustomModel):
    name: Optional[constr(min_length=1)]
    surname: Optional[constr(min_length=1)]
    email: Optional[EmailStr]

    @validator("name")
    def validate_name(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Name should contains only letters"
            )
        return value

    @validator("surname")
    def validate_surname(cls, value):
        if not LETTER_MATCH_PATTERN.match(value):
            raise HTTPException(
                status_code=422, detail="Surname should contains only letters"
            )
        return value


class UserUpdateRole(CustomModel):
    role: UserRole.get_roles_for_update()


class UserShow(CustomModel):
    user_id: UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    roles: set[UserRole]
    created_at: datetime
    updated_at: datetime


class UserOut(CustomModel):
    user_id: UUID


class UserOutForLogin(CustomModel):
    email: EmailStr
    roles: set[UserRole]


class UserInForLogin(CustomModel):
    email: EmailStr
    password: str
