from datetime import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import Optional

from utils.datetime_util import get_local_datetime


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)


class MongoBaseModel(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=get_local_datetime)
    updated_at: datetime = Field(default_factory=get_local_datetime)

    def update_timestamp(self):
        self.updated_at = get_local_datetime()

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True
