from fastapi import APIRouter, Depends

from services.job_seeker_service import JobSeekerService
from models.requests import RegisterJobSeekerRequest, LoginJobSeekerRequest, UploadJobSeekerResumeRequest, UpdateJobSeekerRequest

router = APIRouter(
    prefix="/jobseekers",
    tags=["Job Seekers"],
)


@router.post("/register")
async def register_job_seeker(request: RegisterJobSeekerRequest):
    response = await JobSeekerService.register(request)
    return response


@router.post("/login")
async def login_job_seeker(request: LoginJobSeekerRequest):
    response = await JobSeekerService.login(request)
    return response


@router.put("/{jobseeker_id}/resumes")
async def upload_job_seeker_resume(jobseeker_id: str, request: UploadJobSeekerResumeRequest = Depends(UploadJobSeekerResumeRequest.as_form)):
    response = await JobSeekerService.upload_resume(jobseeker_id, request)
    return response


@router.get("/{jobseeker_id}/profile")
async def get_profile_job_seeker(jobseeker_id: str):
    response = await JobSeekerService.get_profile(jobseeker_id)
    return response


@router.patch("/{jobseeker_id}/profile")
async def update_profile_job_seeker(jobseeker_id: str, request: UpdateJobSeekerRequest):
    response = await JobSeekerService.update_profile(jobseeker_id, request)
    return response
