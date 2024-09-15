import logging
import tempfile
import os
from fastapi import UploadFile, status
from pyresparser import ResumeParser

from repositories.job_seeker_repository import JobSeekerRepository
from models.collections.job_seeker import JobSeeker
from models.requests.job_seeker_request import RegisterJobSeekerRequest
from models.responses.job_seeker_response import RegisterJobSeekerResponse
from utils.password_util import hash

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
                password=hash(request.password)
            )

            result = await JobSeekerRepository.create(jobSeeker)
            log.info(f"Insert job seeker ID : {result.id}")

            return RegisterJobSeekerResponse(
                statusCode=status.HTTP_201_CREATED,
                statusMessage="Register successfully."
            )

        except Exception as e:
            log.error(f"Error: {str(e)}")
            return RegisterJobSeekerResponse(
                statusCode=status.HTTP_500_INTERNAL_SERVER_ERROR,
                statusMessage="An internal server error occurred."
            )

    @staticmethod
    async def login() -> dict:
        return "login jobseeker"

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
