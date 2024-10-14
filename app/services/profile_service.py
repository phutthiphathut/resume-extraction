import logging
from typing import List, Optional
from bson import ObjectId
from fastapi import status


from repositories.job_seeker_repository import JobSeekerRepository
from models.responses import BaseResponse, FailResponse, GetProfileJobSeekerResponseData, SuccessResponse

log = logging.getLogger(__name__)


class ProfileService:
    @staticmethod
    async def get_all_profiles(skill: Optional[str] = None) -> BaseResponse:
        try:
            skills = [s.strip() for s in skill.split(",")] if skill else []
            profiles = await JobSeekerRepository.get_all(skills=skills)

            response_data = []

            for profile in profiles:
                response_data.append(
                    GetProfileJobSeekerResponseData(
                        id=str(profile.id),
                        email=profile.email,
                        first_name=profile.first_name,
                        last_name=profile.last_name,
                        mobile_number=profile.mobile_number,
                        profile=profile.profile
                    )
                )

            return SuccessResponse[List[GetProfileJobSeekerResponseData]](
                status_code=status.HTTP_200_OK,
                status_message="Get all profiles successful.",
                data=response_data
            )

        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def get_profile_by_id(profile_id: str) -> BaseResponse:
        try:
            result = await JobSeekerRepository.get_by_id(ObjectId(profile_id))

            if result is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid job seeker id."
                )

            log.info(
                f"Get profile job seeker ID : {result.id}")

            return SuccessResponse[GetProfileJobSeekerResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Get profile successful.",
                data=GetProfileJobSeekerResponseData(
                    id=str(result.id),
                    email=result.email,
                    first_name=result.first_name,
                    last_name=result.last_name,
                    mobile_number=result.mobile_number,
                    profile=result.profile
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )
