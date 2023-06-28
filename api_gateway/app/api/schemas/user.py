import enum
from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel
from pydantic import constr
from pydantic import EmailStr
from pydantic import Field


class UserRole(str, enum.Enum):
    ROLE_USER = "USER"
    ROLE_MODERATOR = "MODERATOR"
    ROLE_ADMIN = "ADMIN"
    ROLE_SUPERADMIN = "SUPERADMIN"

    @classmethod
    def get_roles_for_update(cls) -> enum.Enum:
        return enum.Enum(
            value="UserRoleForUpdate",
            names={
                key: cls.__members__[key].value
                for key in cls.__members__
                if key not in [cls.ROLE_USER.name, cls.ROLE_SUPERADMIN.name]
            },
        )


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


class UserUpdateRole(CustomModel):
    role: UserRole.get_roles_for_update()


class UserShow(CustomModel):
    user_id: UUID
    name: str
    surname: str
    email: EmailStr
    is_active: bool
    roles: list[UserRole]
    created_at: datetime
    updated_at: datetime


class UserOut(CustomModel):
    user_id: UUID


class UserOutForLogin(CustomModel):
    email: EmailStr
    roles: list[UserRole]
