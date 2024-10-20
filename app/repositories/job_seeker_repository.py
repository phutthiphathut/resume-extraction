import re
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
    async def get_all(skills: Optional[List[str]] = None) -> List[JobSeeker]:
        query = {}
        if skills:
            query = {
                "$and": [
                    {"profile.skills": {"$regex": re.escape(skill), "$options": "i"}} for skill in skills
                ]
            }

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
    async def update(job_seeker: JobSeeker) -> JobSeeker:
        result = await collection.update_one(
            {"_id": job_seeker.id},
            {"$set": job_seeker.model_dump(by_alias=True)}
        )

        if result.modified_count == 1:
            return job_seeker

        return None

    @staticmethod
    async def update_profile(id: ObjectId, profile: Profile, resume_url: str) -> Optional[JobSeeker]:
        result = await collection.find_one_and_update(
            {"_id": id},
            {
                "$set": {
                    "resume_url": resume_url,
                    "profile": profile.model_dump(by_alias=True)
                }
            },
            return_document=True
        )

        if result:
            return JobSeeker(**result)

        return None
