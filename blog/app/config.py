from starlette.config import Config

config = Config('.env')

MONGODB_URL = config('MONGODB_URL', cast=str, default='mongodb://localhost:27017')