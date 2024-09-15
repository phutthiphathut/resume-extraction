from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from configs.app_config import appConfig
from routers import job_seeker_router, profile_router, recruiter_router

app = FastAPI()

origins = [appConfig.CLIENT_ORIGIN_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(job_seeker_router.router)
app.include_router(profile_router.router)
app.include_router(recruiter_router.router)

def run():
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
