import logging
import tempfile
import os
from typing import Any, Dict
from bson import ObjectId
from fastapi import UploadFile, status
from pyresparser import ResumeParser

from models.profile import Profile
from enums.role import Role
from repositories.job_seeker_repository import JobSeekerRepository
from models.collections import JobSeeker
from models.requests import LoginJobSeekerRequest, RegisterJobSeekerRequest, UploadJobSeekerResumeRequest
from models.responses import BaseResponse, FailResponse, LoginJobSeekerResponseData, SuccessResponse, UploadJobSeekerResumeResponseData
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
                password=PasswordUtil.hash(request.password),
                first_name=request.first_name,
                last_name=request.last_name,
                mobile_number=request.mobile_number
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
                "sub": str(existing_job_seeker.id),
                "email": existing_job_seeker.email,
                "role": Role.JOB_SEEKER.value 
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
    async def upload_resume(jobseeker_id: str, request: UploadJobSeekerResumeRequest) -> BaseResponse:
        try:
            temp_file_path = await JobSeekerService._save_temp_file(request.resume_file)

            extracted_data = JobSeekerService._extract_data_from_resume(temp_file_path)

            await JobSeekerService._cleanup_temp_file(temp_file_path)

            profile = Profile.model_validate(extracted_data)
            result = await JobSeekerRepository.update_profile(ObjectId(jobseeker_id), profile)

            if result is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid job seeker id."
                )

            log.info(f"Update profile job seeker ID : {result.id}, {result.profile}")

            return SuccessResponse[UploadJobSeekerResumeResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Resume uploaded successfully.",
                data=UploadJobSeekerResumeResponseData(
                    profile=profile
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

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

    @staticmethod
    async def _save_temp_file(file: UploadFile) -> str:
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
                temp_file.write(file.file.read())
                return temp_file.name
        except Exception as e:
            log.error(f"Error saving file: {str(e)}")
            raise Exception("Error saving file")

    @staticmethod
    def _extract_data_from_resume(file_path: str) -> Dict[str, Any]:
        try:
            data = ResumeParser(file_path).get_extracted_data()
            return data
        except Exception as e:
            log.error(f"Error extracting data from resume: {str(e)}")
            raise Exception("Error extracting data from resume")

    @staticmethod
    async def _cleanup_temp_file(file_path: str) -> None:
        try:
            os.remove(file_path)
        except Exception as e:
            log.error(f"Error removing temporary file: {str(e)}")
            raise Exception("Error removing temporary file")
