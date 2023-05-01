import enum
from typing import Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import ARRAY
from sqlmodel import Column
from sqlmodel import Enum
from sqlmodel import Field
from sqlmodel import SQLModel


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


class User(SQLModel, table=True):
    __tablename__ = "users"

    user_id: Optional[UUID] = Field(default=None, primary_key=True)
    name: str = Field(max_length=15)
    surname: str = Field(max_length=15)
    email: EmailStr = Field(unique=True)
    password: str
    is_active: bool = Field(default=True)
    roles: set[UserRole] = Field(
        sa_column=Column(ARRAY(Enum(UserRole))), default={UserRole.ROLE_USER}
    )

    @property
    def is_admin(self) -> bool:
        return UserRole.ROLE_ADMIN in self.roles

    @property
    def is_moder(self) -> bool:
        return UserRole.ROLE_MODERATOR in self.roles

    def add_role_from_model(self, role_for_add: UserRole):
        if not role_for_add in self.roles:
            return list({*self.roles, role_for_add})

    def remove_role_from_model(self, role_for_delete: UserRole):
        if role_for_delete in self.roles:
            return list({role for role in self.roles if role != role_for_delete})
