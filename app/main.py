from fastapi import FastAPI
from routers import job_seeker_router, profile_router, recruiter_router

app = FastAPI()

app.include_router(job_seeker_router.router)
app.include_router(profile_router.router)
app.include_router(recruiter_router.router)