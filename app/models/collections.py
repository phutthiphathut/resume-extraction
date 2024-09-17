from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator
from bson import ObjectId
from typing import Optional

from utils.datetime_util import DatetimeUtil


class MongoBaseModel(BaseModel):
    id: Optional[ObjectId] = Field(default_factory=ObjectId, alias="_id")
    created_at: datetime = Field(default_factory=DatetimeUtil.get_local_datetime)
    updated_at: datetime = Field(default_factory=DatetimeUtil.get_local_datetime)

    def update_timestamp(self):
        self.updated_at = DatetimeUtil.get_local_datetime()

    @field_validator("id")
    def validate_object_id(cls, value: str) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)

    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True
        arbitrary_types_allowed = True


class JobSeeker(MongoBaseModel):
    email: EmailStr
    password: str


class Recruiter(MongoBaseModel):
    email: EmailStr
    password: str
