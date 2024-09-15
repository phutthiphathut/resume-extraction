from fastapi import APIRouter, HTTPException, UploadFile, status

from services.job_seeker_service import JobSeekerService
from models.responses.job_seeker_response import RegisterJobSeekerResponse
from models.requests.job_seeker_request import RegisterJobSeekerRequest

router = APIRouter(
    prefix="/jobseekers",
    tags=["Job Seekers"],
)


@router.post("/register", response_model=RegisterJobSeekerResponse)
async def register_job_seeker(request: RegisterJobSeekerRequest):
    response = await JobSeekerService.register(request)
    return response


@router.post("/login")
async def login_job_seeker():
    response_data = await JobSeekerService.login()

    return {
        "statusCode": 200,
        "statusMessage": "Login successfully.",
        "data": response_data
    }


@router.post("/{jobseeker_id}/resumes")
async def upload_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    response_data = await JobSeekerService.upload_resume(file)

    return {
        "statusCode": 200,
        "statusMessage": "Extracted data from file successfully.",
        "data": response_data
    }


@router.put("/{jobseeker_id}/resumes")
async def update_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF files are allowed.")

    response_data = await JobSeekerService.update_resume(file)

    return {
        "statusCode": 200,
        "statusMessage": "Extracted data from file successfully.",
        "data": response_data
    }


@router.get("/{jobseeker_id}/profiles")
async def get_profile():
    response_data = await JobSeekerService.get_profile()

    return {
        "statusCode": 200,
        "statusMessage": "Get profile successfully.",
        "data": response_data
    }
