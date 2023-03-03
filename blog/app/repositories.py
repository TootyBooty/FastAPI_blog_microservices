from motor.motor_asyncio import AsyncIOMotorCollection


class BaseRepository:
    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection

    async def create_index(self, index_name: str) -> None:
        await self.collection.create_index(index_name)

    async def drop_index(self, index_name: str) -> None:
        await self.collection.drop_index(index_name)
        
    async def drop_collection(self) -> None:
        await self.collection.drop()


class BlogRepository(BaseRepository):

    async def get_posts(self):
        cursor = self.collection.find({}, {'_id': 0})
        res = []
        for doc in await cursor.to_list(length=20):
            res.append(doc)
        return res


    async def add_post(self):
        await self.collection.insert_one({'test': 'Hello world'})