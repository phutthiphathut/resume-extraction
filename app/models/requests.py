from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, field_validator


class RegisterJobSeekerRequest(BaseModel):
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


class LoginJobSeekerRequest(BaseModel):
    email: EmailStr
    password: str


class UploadJobSeekerResumeRequest(BaseModel):
    resume_file: UploadFile

    @classmethod
    def as_form(cls, resume_file: UploadFile = File(...)):
        if not resume_file.filename.endswith(".pdf"):
            raise ValueError("Only PDF files are allowed.")

        return cls(resume_file=resume_file)
