import logging
from typing import List
from fastapi import status
from bson import ObjectId

from models.collections import Skill
from repositories.skill_repository import SkillRepository
from models.requests import CreateSkillRequest, UpdateSkillRequest
from models.responses import BaseResponse, FailResponse, SuccessResponse, GetSkillResponseData

log = logging.getLogger(__name__)


class SkillService:
    @staticmethod
    async def create_skill(request: CreateSkillRequest) -> BaseResponse:
        try:
            existing_skill = await SkillRepository.get_by_skill_name(request.skill_name)
            if existing_skill:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Skill already exists."
                )

            skill = Skill(
                skill_name=request.skill_name
            )

            result = await SkillRepository.create(skill)
            log.info(f"Insert skill ID : {result.id}")

            return SuccessResponse[GetSkillResponseData](
                status_code=status.HTTP_201_CREATED,
                status_message="Skill created successfully.",
                data=GetSkillResponseData(
                    id=str(result.id),
                    skill_name=result.skill_name
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def get_all_skills() -> BaseResponse:
        try:
            skills = await SkillRepository.get_all()

            response_data = []

            for skill in skills:
                response_data.append(
                    GetSkillResponseData(
                        id=str(skill.id),
                        skill_name=skill.skill_name
                    )
                )

            return SuccessResponse[List[GetSkillResponseData]](
                status_code=status.HTTP_200_OK,
                status_message="Get all skills successful.",
                data=response_data
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def update_skill_by_id(skill_id: str, request: UpdateSkillRequest) -> BaseResponse:
        try:
            skill = await SkillRepository.get_by_id(ObjectId(skill_id))

            if skill is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid skill id."
                )

            existing_skill = await SkillRepository.get_by_skill_name(request.skill_name)
            if existing_skill and existing_skill.id != skill.id:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Skill already exists."
                )
            elif existing_skill and existing_skill.id == skill.id and existing_skill.skill_name == request.skill_name:
                return SuccessResponse[GetSkillResponseData](
                    status_code=status.HTTP_200_OK,
                    status_message="Skill updated successfully.",
                    data=GetSkillResponseData(
                        id=str(skill.id),
                        skill_name=skill.skill_name
                    )
                )

            skill.skill_name = request.skill_name

            result = await SkillRepository.update(skill)

            log.info(f"Updated skill ID: {skill.id}")

            return SuccessResponse[GetSkillResponseData](
                status_code=status.HTTP_200_OK,
                status_message="Skill updated successfully.",
                data=GetSkillResponseData(
                    id=str(result.id),
                    skill_name=result.skill_name
                )
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )

    @staticmethod
    async def delete_skill_by_id(skill_id: str) -> BaseResponse:
        try:
            skill = await SkillRepository.get_by_id(ObjectId(skill_id))

            if skill is None:
                return FailResponse(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    status_message="Invalid skill id."
                )

            await SkillRepository.delete(ObjectId(skill_id))

            log.info(f"Deleted skill id: {skill_id}")

            return SuccessResponse(
                status_code=status.HTTP_200_OK,
                status_message="Skill deleted successfully."
            )
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return FailResponse(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                status_message="An internal server error occurred."
            )
