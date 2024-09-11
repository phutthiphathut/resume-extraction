from typing import Optional

from bson import ObjectId

from models.collections.job_seeker import JobSeeker
from databases.mongo_db import db

COLLECTION_NAME = "job_seekers"
collection = db[COLLECTION_NAME]


class JobSeekerRepository:
    @staticmethod
    async def get_by_email(email: str) -> Optional[JobSeeker]:
        result = await collection.find_one({"email": email})

        if result:
            return JobSeeker(**result)

        return None

    @staticmethod
    async def create(job_seeker: JobSeeker) -> JobSeeker:
        result = await collection.insert_one(job_seeker.model_dump(by_alias=True))
        job_seeker.id = result.inserted_id

        return job_seeker

    @staticmethod
    async def update(job_seeker: JobSeeker) -> Optional[JobSeeker]:
        result = await collection.find_one_and_update(
            {"_id": job_seeker.id},
            {"$set": job_seeker.model_dump(by_alias=True)},
            return_document=True
        )

        if result:
            return JobSeeker(**result)

        return None
