from fastapi import APIRouter
from services.recruiter_service import RecruiterService
from models.requests import RegisterRecruiterRequest, LoginRecruiterRequest

router = APIRouter(
    prefix="/recruiters",
    tags=["Recruiters"],
)

service = RecruiterService()

@router.post("/register")
async def register_recruiter(request: RegisterRecruiterRequest):
    response = await RecruiterService.register(request)
    return response


@router.post("/login")
async def login_job_seeker(request: LoginRecruiterRequest):
    response = await RecruiterService.login(request)
    return response
