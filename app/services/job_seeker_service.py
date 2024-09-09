import tempfile
import os
from fastapi import UploadFile
from pyresparser import ResumeParser

from repositories.job_seeker_repository import insert_job_seeker
from models.collections.job_seeker import JobSeeker
from models.requests.job_seeker_request import RegisterJobSeekerRequest
from models.responses.job_seeker_response import RegisterJobSeekerResponse

async def register_job_seeker(request: RegisterJobSeekerRequest) -> RegisterJobSeekerResponse:
    entity = JobSeeker(
        email=request.email,
        password=request.password
    )

    insert_id = await insert_job_seeker(entity)
    print(f"Insert job seeker ID : {insert_id}")

    return RegisterJobSeekerResponse(
        statusCode=200,
        statusMessage="Register successfully."
    )

async def login_job_seeker() -> dict:
    return "login jobseeker"

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

async def get_profile() -> dict:

    return "get profile"
