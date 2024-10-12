from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from exceptions.exception_handler import validation_exception_handler, value_error_handler
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

app.add_exception_handler(ValueError, value_error_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)

@app.get("/")
async def health_check():
    return "Hello"