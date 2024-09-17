from typing import Optional
from pymongo.collection import Collection

from models.collections import Recruiter
from databases.mongo_db import database

COLLECTION_NAME = "recruiter"
collection: Collection = database[COLLECTION_NAME]


class RecruiterRepository:
    @staticmethod
    async def get_by_email(email: str) -> Optional[Recruiter]:
        result = await collection.find_one({"email": email})
        
        if result:
            return Recruiter(**result)

        return None

    @staticmethod
    async def create(recruiter: Recruiter) -> Recruiter:
        result = await collection.insert_one(recruiter.model_dump(by_alias=True))
        recruiter.id = result.inserted_id

        return recruiter

    @staticmethod
    async def update(recruiter: Recruiter) -> Optional[Recruiter]:
        result = await collection.find_one_and_update(
            {"_id": recruiter.id},
            {"$set": recruiter.model_dump(by_alias=True)},
            return_document=True
        )

        if result:
            return Recruiter(**result)

        return None
