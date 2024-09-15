import logging
from motor.motor_asyncio import AsyncIOMotorClient

from configs.app_config import appConfig

log = logging.getLogger(__name__)

mongo_client = AsyncIOMotorClient(appConfig.MONGO_DB_URL)
log.info("Connected to MongoDB successfully!")

database = mongo_client[appConfig.MONGO_DB_NAME]
