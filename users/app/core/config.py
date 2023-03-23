from starlette.config import Config

config = Config('.env')


POSTGRES_URL = config('POSTGRES_URL', cast=str, default='postgresql+asyncpg://postgres:postgres@0.0.0.0:5432/users')
