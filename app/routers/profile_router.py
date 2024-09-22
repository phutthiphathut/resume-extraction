from typing import Optional
from fastapi import APIRouter, Query
from services.profile_service import ProfileService

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)

@router.get("")
async def get_all_profiles(skill: Optional[str] = Query(None)):
    response = await ProfileService.get_all_profiles(skill=skill)
    return response

@router.get("/{profile_id}")
async def get_profile_by_id(profile_id: str):
    response = await ProfileService.get_profile_by_id(profile_id)
    return response
