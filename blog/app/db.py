from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_URL


client = AsyncIOMotorClient(MONGODB_URL, uuidRepresentation='standard')

blog_db = client.blog_db

blog_collection = blog_db.blog_collection