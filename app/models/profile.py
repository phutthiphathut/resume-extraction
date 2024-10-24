from typing import List, Optional
from pydantic import BaseModel


class Profile(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    mobile_number: Optional[str] = None
    skills: Optional[List[str]] = None
    college_name: Optional[str] = None
    degree: Optional[str] = None
    designation: Optional[List[str]] = None
    experience: Optional[List[str]] = None
    company_names: Optional[List[str]] = None
    no_of_pages: Optional[int] = None
    total_experience: Optional[float] = None
