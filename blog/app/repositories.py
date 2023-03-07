from motor.motor_asyncio import AsyncIOMotorCollection
from uuid6 import uuid6
from pymongo import ReturnDocument

from schemas import *


class BaseRepository:
    def __init__(self, collection:AsyncIOMotorCollection):
        self.collection = collection

    async def _create_index(self, index_name: str) -> None:
        await self.collection.create_index(index_name)

    async def _drop_index(self, index_name: str) -> None:
        await self.collection.drop_index(index_name)
        
    async def _drop_collection(self) -> None:
        await self.collection.drop()


class BlogRepository(BaseRepository):

    async def get_posts(self, limit:int = None) -> list[Post]:
        cursor = self.collection.find({})
        res = []
        for doc in await cursor.to_list(length=limit):
            res.append(doc)
        return res


    async def create_post(self, post:PostIn, current_time) -> Post:
        post_data = Post(
            post_id=uuid6(),
            creator=post.creator,
            title=post.title,
            content=post.content,
            created_at=current_time,
            updated_at=current_time
        )

        values = {**post_data.dict()}
        values['_id'] = values.pop('post_id')
        await self.collection.insert_one(values)
        return post_data


    async def get_post(self, post_id) -> Post|None:
        doc = await self.collection.find_one({'_id': post_id}, {'_id': 0, 'post_id': post_id,
                                                'creator': 1, 'title': 1,'content': 1,'comments': 1,'created_at': 1, 'updated_at': 1})
        return doc
    

    async def update_post(self, post_id, current_time, update_data) -> Post|None:
        update_data['updated_at'] = current_time
        doc = await self.collection.find_one_and_update({'_id': post_id}, {'$set': update_data},
                                                        {'_id': 0, 'post_id':post_id,'creator': 1,
                                                        'title': 1,'content': 1,'comments': 1,'created_at': 1, 'updated_at': 1},
                                                        return_document=ReturnDocument.AFTER)
        return doc
    

    async def delete_post(self, post_id) -> Post|None:
        doc = await self.collection.find_one_and_delete({'_id': post_id}, {'_id': 0, 'post_id': post_id,
                                                            'creator': 1, 'title': 1,'content': 1,'comments': 1,'created_at': 1, 'updated_at': 1})
        return doc