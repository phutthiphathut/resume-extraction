from fastapi import APIRouter, HTTPException, UploadFile
from services.job_seeker_service import JobSeekerService

router = APIRouter(
    prefix="/jobseekers",
    tags=["Job Seekers"],
)

service = JobSeekerService()

@router.post("/register")
async def register_job_seeker():
    response_data = await service.register_job_seeker()

    return {
        "statusCode": 200, 
        "statusMessage": "Register successfully.", 
        "data": response_data
    }

@router.post("/login")
async def login_job_seeker():
    response_data = await service.login_job_seeker()

    return {
        "statusCode": 200, 
        "statusMessage": "Login successfully.", 
        "data": response_data
    }

@router.post("/{jobseeker_id}/resumes")
async def upload_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    response_data = await service.upload_resume(file)

    return {
        "statusCode": 200, 
        "statusMessage": "Extracted data from file successfully.", 
        "data": response_data
    }

@router.put("/{jobseeker_id}/resumes")
async def update_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    response_data = await service.update_resume(file)

    return {
        "statusCode": 200, 
        "statusMessage": "Extracted data from file successfully.", 
        "data": response_data
    }

@router.get("/{jobseeker_id}/profiles")
async def get_profile():
    
    response_data = await service.get_profile()

    return {
        "statusCode": 200, 
        "statusMessage": "Get profile successfully.", 
        "data": response_data
    }
