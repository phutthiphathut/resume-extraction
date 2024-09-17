import logging

from fastapi import status

from enums.role import Role
from repositories.recruiter_repository import RecruiterRepository
from models.collections import Recruiter
from models.requests import LoginRecruiterRequest, RegisterRecruiterRequest
from models.responses import BaseResponse, FailResponse, LoginRecruiterResponseData, SuccessResponse
from utils.password_util import PasswordUtil
from utils.jwt_util import JwtUtil

log = logging.getLogger(__name__)


class RecruiterService:
    @staticmethod
    async def register(request: RegisterRecruiterRequest) -> BaseResponse:
        try:
            existing_recruiter = await RecruiterRepository.get_by_email(request.email)

            if existing_recruiter:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Email is already registered."
                )

            recruiter = Recruiter(
                email=request.email,
                password=PasswordUtil.hash(request.password)
            )

            result = await RecruiterRepository.create(recruiter)
            log.info(f"Insert job seeker ID : {result.id}")

            return SuccessResponse(
                status_code=status.HTTP_201_CREATED,
                status_message="Register successful."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def login(request: LoginRecruiterRequest) -> BaseResponse:
        try:
            existing_recruiter = await RecruiterRepository.get_by_email(request.email)

            if existing_recruiter is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid email or password."
                )

            if not PasswordUtil.verify(request.password, existing_recruiter.password):
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid email or password."
                )

            payload = {
                "sub": str(existing_recruiter.id),
                "email": existing_recruiter.email,
                "role": Role.RECRUITER.value 
            }

            token = JwtUtil.create(payload)

            return SuccessResponse[LoginRecruiterResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Login successful.",
                data=LoginRecruiterResponseData(
                    access_token=token
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )
