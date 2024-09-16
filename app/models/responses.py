from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel

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
    name: str
    email: str
    mobile_number: str
    skills: List[str]
    college_name: Optional[str] = None
    degree: List[str]
    designation: List[str]
    experience: List[str]
    company_names: List[str]
    no_of_pages: int
    total_experience: float
