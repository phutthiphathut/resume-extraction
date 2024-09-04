from fastapi import APIRouter
from services.recruiter_service import RecruiterService

router = APIRouter(
    prefix="/recruiters",
    tags=["Recruiters"],
)

service = RecruiterService()

@router.post("/register")
async def register_recruiter():
    response_data = await service.register_recruiter()

    return {
        "statusCode": 200, 
        "statusMessage": "Register successfully.", 
        "data": response_data
    }

@router.post("/login")
async def login_recruiter():
    response_data = await service.login_recruiter()

    return {
        "statusCode": 200, 
        "statusMessage": "Login successfully.", 
        "data": response_data
    }