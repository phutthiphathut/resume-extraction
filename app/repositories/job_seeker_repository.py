from typing import Optional, List
from bson import ObjectId
from pymongo.collection import Collection

from models.profile import Profile
from models.collections import JobSeeker
from databases.mongo_db import database

COLLECTION_NAME = "job_seekers"
collection: Collection = database[COLLECTION_NAME]


class JobSeekerRepository:
    @staticmethod
    async def get_all(skill: Optional[str] = None) -> List[JobSeeker]:
        query = {}
        if skill:
            query = {"profile.skills": skill}
       
        results = await collection.find(query).to_list(None)

        if results:
            return [JobSeeker(**result) for result in results]

        return []

    @staticmethod
    async def get_by_email(email: str) -> Optional[JobSeeker]:
        result = await collection.find_one({"email": email})

        if result:
            return JobSeeker(**result)

        return None

    @staticmethod
    async def get_by_id(id: ObjectId) -> Optional[JobSeeker]:
        result = await collection.find_one({"_id": id})

        if result:
            return JobSeeker(**result)

        return None

    @staticmethod
    async def create(job_seeker: JobSeeker) -> JobSeeker:
        result = await collection.insert_one(job_seeker.model_dump(by_alias=True))
        job_seeker.id = result.inserted_id

        return job_seeker

    @staticmethod
    async def update_profile(id: ObjectId, profile: Profile) -> Optional[JobSeeker]:
        result = await collection.find_one_and_update(
            {"_id": id},
            {"$set": {"profile": profile.model_dump(by_alias=True)}},
            return_document=True
        )

        if result:
            return JobSeeker(**result)

        return None
