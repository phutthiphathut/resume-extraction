from fastapi import APIRouter, Depends

from services.skill_service import SkillService
from models.requests import CreateSkillRequest, UpdateSkillRequest

router = APIRouter(
    prefix="/skills",
    tags=["Skills"],
)

@router.get("")
async def get_all_skills():
    response = await SkillService.get_all_skills()
    return response

@router.post("")
async def create_skill(request: CreateSkillRequest):
    response = await SkillService.create_skill(request)
    return response

@router.put("/{skill_id}")
async def update_skill_by_id(skill_id: str, request: UpdateSkillRequest):
    response = await SkillService.update_skill_by_id(skill_id, request)
    return response

@router.delete("/{skill_id}")
async def delete_skill_by_id(skill_id: str):
    response = await SkillService.delete_skill_by_id(skill_id)
    return response