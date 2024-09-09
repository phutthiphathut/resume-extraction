from pydantic import BaseModel

class JobSeeker(BaseModel):
    email: str
    password: str
