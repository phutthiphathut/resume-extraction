from fastapi import APIRouter
from services.profile_service import ProfileService

router = APIRouter(
    prefix="/profiles",
    tags=["Profiles"],
)

service = ProfileService()

@router.get("")
async def get_profile():
    
    response_data = await service.get_profile()

    return {
        "statusCode": 200, 
        "statusMessage": "Get profile successfully.", 
        "data": response_data
    }

@router.get("/{profile_id}")
async def get_profile_by_id():
    
    response_data = await service.get_profile_by_id()

    return {
        "statusCode": 200, 
        "statusMessage": "Get profile by id successfully.", 
        "data": response_data
    }