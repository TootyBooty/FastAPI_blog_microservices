import pathlib

from pydantic import BaseSettings, EmailStr

root = pathlib.Path(__file__).parent.parent

env_file = root / '.env'


class Settings(BaseSettings):

    project_root: pathlib.Path = root
    secret_key: str = 'very_secret_key'
    postgres_url: str = "postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/users"
    token_url: str = "/auth/login"
    
    # superadmin_data
    superadmin_name: str = 'root'
    superadmin_surname: str = 'root'
    superadmin_email: EmailStr = 'root@root.root'
    superadmin_password: str = 'root'

    class Config:
        env_file = '.env'


Config = Settings(_env_file=env_file)