import logging
import tempfile
import os
from fastapi import UploadFile, status
from pyresparser import ResumeParser

from repositories.job_seeker_repository import JobSeekerRepository
from models.collections import JobSeeker
from models.requests import LoginJobSeekerRequest, RegisterJobSeekerRequest
from models.responses import BaseResponse, FailResponse, LoginJobSeekerResponseData, SuccessResponse
from utils.password_util import PasswordUtil
from utils.jwt_util import JwtUtil

log = logging.getLogger(__name__)


class JobSeekerService:
    @staticmethod
    async def register(request: RegisterJobSeekerRequest) -> BaseResponse:
        try:
            existing_job_seeker = await JobSeekerRepository.get_by_email(request.email)

            if existing_job_seeker:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Email is already registered."
                )

            jobSeeker = JobSeeker(
                email=request.email,
                password=PasswordUtil.hash(request.password)
            )

            result = await JobSeekerRepository.create(jobSeeker)
            log.info(f"Insert job seeker ID : {result.id}")

            return SuccessResponse(
                status_code=status.HTTP_201_CREATED,
                status_message="Register successful."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def login(request: LoginJobSeekerRequest) -> BaseResponse:
        try:
            existing_job_seeker = await JobSeekerRepository.get_by_email(request.email)

            if existing_job_seeker is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid email or password."
                )

            if not PasswordUtil.verify(request.password, existing_job_seeker.password):
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid email or password."
                )

            payload = {
                "sub": existing_job_seeker.id,
                "email": existing_job_seeker.email
            }

            token = JwtUtil.create(payload)

            return SuccessResponse[LoginJobSeekerResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Login successful.",
                data=LoginJobSeekerResponseData(
                    access_token=token
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
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
