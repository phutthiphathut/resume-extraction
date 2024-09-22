from fastapi import APIRouter
from services.profile_service import ProfileService

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)

@router.get("")
async def get_all_profiles():
    response = await ProfileService.get_all_profiles()
    return response

@router.get("/{profile_id}")
async def get_profile_by_id(profile_id: str):
    response = await ProfileService.get_profile_by_id(profile_id)
    return response
