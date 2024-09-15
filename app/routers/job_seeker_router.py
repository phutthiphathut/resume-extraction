from fastapi import APIRouter, HTTPException, UploadFile

from services.job_seeker_service import JobSeekerService
from models.requests import RegisterJobSeekerRequest, LoginJobSeekerRequest
from models.responses import LoginJobSeekerResponse, RegisterJobSeekerResponse

router = APIRouter(
    prefix="/jobseekers",
    tags=["Job Seekers"],
)


@router.post("/register", response_model=RegisterJobSeekerResponse)
async def register_job_seeker(request: RegisterJobSeekerRequest):
    response = await JobSeekerService.register(request)
    return response


@router.post("/login", response_model=LoginJobSeekerResponse)
async def login_job_seeker(request: LoginJobSeekerRequest):
    response = await JobSeekerService.login(request)
    return response


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
