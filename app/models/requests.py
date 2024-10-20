from typing import List, Optional
from fastapi import File, UploadFile
from pydantic import BaseModel, EmailStr, field_validator


class RegisterJobSeekerRequest(BaseModel):
    email: EmailStr
    password: str
    first_name: str
    last_name: str
    mobile_number: str

    @field_validator('password')
    def validate_password(cls, value: str) -> str:
        if len(value) < 8:
            raise ValueError('Password must be at least 8 characters long')
        if not any(char.isalpha() for char in value):
            raise ValueError('Password must contain at least one letter')
        if not any(char.isdigit() for char in value):
            raise ValueError('Password must contain at least one number')

        return value

    @field_validator('first_name')
    def validate_first_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError('First name must be at least 2 characters long')
        if not value.isalpha():
            raise ValueError(
                'First name must contain only alphabetic characters')
        return value

    @field_validator('last_name')
    def validate_last_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError('Last name must be at least 2 characters long')
        if not value.isalpha():
            raise ValueError(
                'Last name must contain only alphabetic characters')
        return value

    @field_validator('mobile_number')
    def validate_mobile_number(cls, value: str) -> str:
        if len(value) < 10 or len(value) > 15:
            raise ValueError(
                'Mobile number must be between 10 and 15 digits long')
        if not value.isdigit():
            raise ValueError('Mobile number must contain only digits')
        return value


class LoginJobSeekerRequest(BaseModel):
    email: EmailStr
    password: str


class UploadJobSeekerResumeRequest(BaseModel):
    resume_file: UploadFile

    @classmethod
    def as_form(cls, resume_file: UploadFile = File(...)):
        if not resume_file.filename.endswith(".pdf"):
            raise ValueError("Only PDF file is allowed.")

        return cls(resume_file=resume_file)


class RegisterRecruiterRequest(BaseModel):
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


class LoginRecruiterRequest(BaseModel):
    email: EmailStr
    password: str


class UpdateJobSeekerRequest(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    mobile_number: str
    skills: Optional[List[str]] = None
    college_name: Optional[str] = None
    degree: Optional[List[str]] = None
    designation: Optional[List[str]] = None

    @field_validator('first_name')
    def validate_first_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError('First name must be at least 2 characters long')
        if not value.isalpha():
            raise ValueError(
                'First name must contain only alphabetic characters')
        return value

    @field_validator('last_name')
    def validate_last_name(cls, value: str) -> str:
        if len(value) < 2:
            raise ValueError('Last name must be at least 2 characters long')
        if not value.isalpha():
            raise ValueError(
                'Last name must contain only alphabetic characters')
        return value

    @field_validator('mobile_number')
    def validate_mobile_number(cls, value: str) -> str:
        if len(value) < 10 or len(value) > 15:
            raise ValueError(
                'Mobile number must be between 10 and 15 digits long')
        if not value.isdigit():
            raise ValueError('Mobile number must contain only digits')
        return value
