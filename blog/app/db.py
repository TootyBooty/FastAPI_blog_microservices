from config import Config
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(Config.MONGODB_URL, uuidRepresentation="standard")

blog_db = client.blog_db

blog_collection = blog_db.blog_collection
