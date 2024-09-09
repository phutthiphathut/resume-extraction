from pydantic import BaseModel

class RegisterJobSeekerRequest(BaseModel):
    email: str
    password: str
