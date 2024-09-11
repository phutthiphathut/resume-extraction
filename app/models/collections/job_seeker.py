from pydantic import EmailStr

from models.collections.mongo_base_model import MongoBaseModel


class JobSeeker(MongoBaseModel):
    email: EmailStr
    password: str
