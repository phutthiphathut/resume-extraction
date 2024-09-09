from models.collections.job_seeker import JobSeeker
from databases.mongodb import JobSeekerCollection

async def insert_job_seeker(entity: JobSeeker) -> str:
    job_seeker_data = entity.model_dump()
    result = await JobSeekerCollection.insert_one(job_seeker_data)
    return str(result.inserted_id)
