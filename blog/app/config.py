from pydantic import BaseSettings, EmailStr


class Settings(BaseSettings):
    API_GATEWAY_TOKEN: str
    MONGODB_URL: str = "mongodb://localhost:27017"
    TOKEN_URL: str = "/auth/login"

    class Config:
        env_file = '.env'

Config = Settings()