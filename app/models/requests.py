from pydantic import BaseModel, EmailStr, field_validator


class BaseRequest(BaseModel):
    class Config:
        str_strip_whitespace = True


class RegisterJobSeekerRequest(BaseRequest):
    email: EmailStr
    password: str

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one number')

        return value

class LoginJobSeekerRequest(BaseRequest):
    email: EmailStr
    password: str
