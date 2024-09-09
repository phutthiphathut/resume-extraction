from motor.motor_asyncio import AsyncIOMotorClient
from configs.app_config import appConfig

mongo_client = AsyncIOMotorClient(appConfig.MONGO_DB_URL)
print("Connected to MongoDB successfully!")

db = mongo_client[appConfig.MONGO_DB_NAME]

JobSeekerCollection = db["job_seekers"]
