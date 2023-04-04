from pydantic import BaseSettings


class Settings(BaseSettings):
    USERS_SERVICE_URL: str = 'http://127.0.0.1'
    BLOG_SERVICE_URL: str = 'http://127.0.0.1'
    GATEWAY_TIMEOUT: int = 10
    
    API_GATEWAY_TOKEN: str
    SECRET_KEY: str = "secret_key"

    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = '.env'


Config = Settings()