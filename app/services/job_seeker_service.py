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
from repositories.skill_repository import SkillRepository
from models.collections import JobSeeker, Skill
from models.requests import LoginJobSeekerRequest, RegisterJobSeekerRequest, UpdateJobSeekerRequest, UploadJobSeekerResumeRequest
from models.responses import BaseResponse, FailResponse, GetProfileJobSeekerResponseData, LoginJobSeekerResponseData, SuccessResponse
from utils.password_util import PasswordUtil
from utils.jwt_util import JwtUtil
from utils.storage_util import StorageUtil

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

            extracted_data = JobSeekerService._extract_data_from_resume(
                temp_file_path)

            resume_url = JobSeekerService._upload_file_to_storage(
                temp_file_path, jobseeker_id)

            await JobSeekerService._cleanup_temp_file(temp_file_path)

            profile = Profile.model_validate(extracted_data)
            result = await JobSeekerRepository.update_profile(ObjectId(jobseeker_id), profile, resume_url)

            if result is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid job seeker id."
                )

            log.info(
                f"Update profile job seeker ID : {result.id}, {result.profile}")
            
            for skill_name in profile.skills:
                skill = await SkillRepository.get_by_skill_name(skill_name)
                if skill is None:
                    new_skill = Skill(skill_name=skill_name)
                    await SkillRepository.create(new_skill)

            return SuccessResponse(
                status_code=status.HTTP_200_OK,
                status_message="Resume uploaded successfully."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def get_profile(jobseeker_id: str) -> BaseResponse:
        try:
            result = await JobSeekerRepository.get_by_id(ObjectId(jobseeker_id))

            if result is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid job seeker id."
                )

            log.info(
                f"Get profile job seeker ID : {result.id}")

            return SuccessResponse[GetProfileJobSeekerResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Get profile successful.",
                data=GetProfileJobSeekerResponseData(
                    id=str(result.id),
                    email=result.email,
                    first_name=result.first_name,
                    last_name=result.last_name,
                    mobile_number=result.mobile_number,
                    resume_url=result.resume_url,
                    profile=result.profile
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def update_profile(jobseeker_id: str, request: UpdateJobSeekerRequest) -> BaseResponse:
        try:
            job_seeker = await JobSeekerRepository.get_by_id(ObjectId(jobseeker_id))
        
            if job_seeker is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid job seeker id."
                )

            job_seeker.email = request.email
            job_seeker.first_name = request.first_name
            job_seeker.last_name = request.last_name
            job_seeker.mobile_number = request.mobile_number
            job_seeker.profile.skills = request.skills
            job_seeker.profile.college_name = request.college_name
            job_seeker.profile.degree = request.degree
            job_seeker.profile.designation = request.designation

            await JobSeekerRepository.update(job_seeker)

            log.info(
                f"Update job seeker ID : {job_seeker.id}")

            return SuccessResponse(
                status_code=status.HTTP_200_OK,
                status_message="Job seeker profile updated successfully."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

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

    @staticmethod
    def _upload_file_to_storage(file_path: str, file_name: str) -> str:
        try:
            storage = StorageUtil()
            object_name = f"resumes/{file_name}.pdf"

            storage.upload_file(file_path, object_name)

            file_url = storage.get_cdn_file_url(object_name)

            return file_url
        except Exception as e:
            log.error(f"Error uploading file to storage: {str(e)}")
            raise Exception("Error uploading file to storage")
