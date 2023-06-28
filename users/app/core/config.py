from datetime import tzinfo

import pytz
from pydantic import BaseSettings
from pydantic import EmailStr


class Settings(BaseSettings):
    API_GATEWAY_TOKEN: str = ""
    POSTGRES_URL: str = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/users"
    TOKEN_URL: str = "/auth/login"

    # superadmin_data
    superadmin_name: str = "root"
    superadmin_surname: str = "root"
    superadmin_email: EmailStr = "root@root.root"
    superadmin_password: str = "root"

    # time
    TIMEZONE: tzinfo = pytz.timezone("Europe/Moscow")

    class Config:
        env_file = ".env"


Config = Settings()
