from typing import Generic, Optional, TypeVar
from pydantic import BaseModel

T = TypeVar('T')

class BaseResponse(Generic[T], BaseModel):
    statusCode: int
    statusMessage: str
    data: Optional[T] = None

class LoginJobSeekerResponse(BaseResponse):
    pass
