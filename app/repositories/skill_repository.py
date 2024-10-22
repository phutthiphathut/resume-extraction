from typing import Optional, List
from bson import ObjectId
from pymongo.collection import Collection

from models.collections import Skill
from databases.mongo_db import database

COLLECTION_NAME = "skills"
collection: Collection = database[COLLECTION_NAME]


class SkillRepository:
    @staticmethod
    async def get_by_skill_name(skill_name: str) -> Optional[Skill]:
        result = await collection.find_one({"skill_name": {"$regex": f"^{skill_name}$", "$options": "i"}})

        if result:
            return Skill(**result)

        return None

    @staticmethod
    async def get_by_id(id: ObjectId) -> Optional[Skill]:
        result = await collection.find_one({"_id": id})

        if result:
            return Skill(**result)

        return None

    @staticmethod
    async def get_all() -> List[Skill]:
        results = await collection.find().to_list(length=None)

        return [Skill(**result) for result in results]

    @staticmethod
    async def create(skill: Skill) -> Skill:
        result = await collection.insert_one(skill.model_dump(by_alias=True))
        skill.id = result.inserted_id

        return skill

    @staticmethod
    async def update(skill: Skill) -> Optional[Skill]:
        result = await collection.update_one(
            {"_id": skill.id},
            {"$set": skill.model_dump(by_alias=True)}
        )

        if result.modified_count == 1:
            return skill

        return None

    @staticmethod
    async def delete(id: ObjectId) -> bool:
        result = await collection.delete_one({"_id": id})

        return result.deleted_count > 0
