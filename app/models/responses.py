from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel

from models.profile import Profile

T = TypeVar('T')


class BaseResponse(BaseModel):
    status_code: int
    status_message: Any


class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None


class FailResponse(BaseResponse):
    pass


class LoginJobSeekerResponseData(BaseModel):
    access_token: str


class UploadJobSeekerResumeResponseData(BaseModel):
    profile: Profile


class LoginRecruiterResponseData(BaseModel):
    access_token: str
