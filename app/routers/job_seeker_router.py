from fastapi import APIRouter, HTTPException, UploadFile
from services.job_seeker_service import get_profile, login_job_seeker, register_job_seeker, update_resume, upload_resume
from models.responses.job_seeker_response import RegisterJobSeekerResponse
from models.requests.job_seeker_request import RegisterJobSeekerRequest

router = APIRouter(
    prefix="/jobseekers",
    tags=["Job Seekers"],
)

@router.post("/register", response_model=RegisterJobSeekerResponse)
async def register_job_seeker_handler(request: RegisterJobSeekerRequest):
    await register_job_seeker(request)

    return RegisterJobSeekerResponse(
        statusCode=200,
        statusMessage="Register successfully."
    )

@router.post("/login")
async def login_job_seekerr_handler():
    response_data = await login_job_seeker()

    return {
        "statusCode": 200, 
        "statusMessage": "Login successfully.", 
        "data": response_data
    }

@router.post("/{jobseeker_id}/resumes")
async def upload_resumer_handler(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    response_data = await upload_resume(file)

    return {
        "statusCode": 200, 
        "statusMessage": "Extracted data from file successfully.", 
        "data": response_data
    }

@router.put("/{jobseeker_id}/resumes")
async def update_resumer_handler(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    response_data = await update_resume(file)

    return {
        "statusCode": 200, 
        "statusMessage": "Extracted data from file successfully.", 
        "data": response_data
    }

@router.get("/{jobseeker_id}/profiles")
async def get_profiler_handler():
    
    response_data = await get_profile()

    return {
        "statusCode": 200, 
        "statusMessage": "Get profile successfully.", 
        "data": response_data
    }
