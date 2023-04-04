from motor.motor_asyncio import AsyncIOMotorClient

from config import Config


client = AsyncIOMotorClient(Config.MONGODB_URL, uuidRepresentation='standard')

blog_db = client.blog_db

blog_collection = blog_db.blog_collection