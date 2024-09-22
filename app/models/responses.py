from typing import Any, Generic, Optional, TypeVar
from pydantic import BaseModel, EmailStr

from models.profile import Profile

T = TypeVar('T')


class BaseResponse(BaseModel):
    status_code: int
    status_message: Any


class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None


class FailResponse(BaseResponse):
    pass


class GetProfileJobSeekerResponseData(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    mobile_number: str
    profile: Optional[Profile] = None


class LoginJobSeekerResponseData(BaseModel):
    access_token: str


class LoginRecruiterResponseData(BaseModel):
    access_token: str
