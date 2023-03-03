from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_URL


client = AsyncIOMotorClient(MONGODB_URL)

blog_db = client.blog_db

blog_collection = blog_db.blog_collection