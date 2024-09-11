import tempfile
import os
from fastapi import UploadFile, status
from pyresparser import ResumeParser

from repositories.job_seeker_repository import JobSeekerRepository
from models.collections.job_seeker import JobSeeker
from models.requests.job_seeker_request import RegisterJobSeekerRequest
from models.responses.job_seeker_response import RegisterJobSeekerResponse


class JobSeekerService:
    @staticmethod
    async def register(request: RegisterJobSeekerRequest) -> RegisterJobSeekerResponse:
        # existing_job_seeker = await JobSeekerRepository.get_by_email(request.email)

        # if existing_job_seeker:
        #     return RegisterJobSeekerResponse(
        #         statusCode=status.HTTP_400_BAD_REQUEST,
        #         statusMessage="Email is already registered."
        #     )

        jobSeeker = JobSeeker(
            email=request.email,
            password=request.password
        )

        result = await JobSeekerRepository.create(jobSeeker)
        print(f"Insert job seeker ID : {result.id}")

        return RegisterJobSeekerResponse(
            statusCode=status.HTTP_201_CREATED,
            statusMessage="Register successfully."
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
