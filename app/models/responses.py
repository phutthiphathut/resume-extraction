from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(BaseModel):
    status_code: int
    status_message: str

class SuccessResponse(BaseResponse, Generic[T]):
    data: Optional[T] = None

class FailResponse(BaseResponse):
    pass

class LoginJobSeekerResponseData(BaseModel):
    access_token: str
