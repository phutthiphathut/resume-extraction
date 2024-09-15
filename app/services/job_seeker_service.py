import logging
import tempfile
import os
from fastapi import UploadFile, status
from pyresparser import ResumeParser

from repositories.job_seeker_repository import JobSeekerRepository
from models.collections import JobSeeker
from models.requests import LoginJobSeekerRequest, RegisterJobSeekerRequest
from models.responses import LoginJobSeekerResponse, RegisterJobSeekerResponse
from utils.password_util import PasswordUtil
from utils.jwt_util import JwtUtil

log = logging.getLogger(__name__)


class JobSeekerService:
    @staticmethod
    async def register(request: RegisterJobSeekerRequest) -> RegisterJobSeekerResponse:
        try:
            existing_job_seeker = await JobSeekerRepository.get_by_email(request.email)

            if existing_job_seeker:
                return RegisterJobSeekerResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    statusMessage="Email is already registered."
                )

            jobSeeker = JobSeeker(
                email=request.email,
                password=PasswordUtil.hash(request.password)
            )

            result = await JobSeekerRepository.create(jobSeeker)
            log.info(f"Insert job seeker ID : {result.id}")

            return RegisterJobSeekerResponse(
                statusCode=status.HTTP_201_CREATED,
                statusMessage="Register successful."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return RegisterJobSeekerResponse(
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                statusMessage="An internal server error occurred."
            )

    @staticmethod
    async def login(request: LoginJobSeekerRequest) -> LoginJobSeekerResponse:
        try:
            existing_job_seeker = await JobSeekerRepository.get_by_email(request.email)

            if existing_job_seeker is None:
                return LoginJobSeekerResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    statusMessage="Invalid email or password."
                )

            if not PasswordUtil.verify(request.password, existing_job_seeker.password):
                return LoginJobSeekerResponse(
                    statusCode=status.HTTP_400_BAD_REQUEST,
                    statusMessage="Invalid email or password."
                )

            payload = {
                "sub": existing_job_seeker.id,
                "email": existing_job_seeker.email
            }
            
            token = JwtUtil.create(payload)

            return LoginJobSeekerResponse(
                statusCode=status.HTTP_200_OK,
                statusMessage="Login successful."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return LoginJobSeekerResponse(
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                statusMessage="An internal server error occurred."
            )

    @staticmethod
    async def upload_resume(file: UploadFile) -> dict:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name
        print(temp_file_path)

        # Extract data from the resume
        data = ResumeParser(temp_file_path).get_extracted_data()

        # Clean up the temporary file
        os.remove(temp_file_path)

        return data

    @staticmethod
    async def update_resume(file: UploadFile) -> dict:
        # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name
        print(temp_file_path)

        # Extract data from the resume
        data = ResumeParser(temp_file_path).get_extracted_data()

        # Clean up the temporary file
        os.remove(temp_file_path)

        return data

    @staticmethod
    async def get_profile() -> dict:
        return "get profile"
