from fastapi import APIRouter, HTTPException, UploadFile
from services.resume_service import ResumeService

router = APIRouter(
    prefix="/resumes",
    tags=["resumes"],
)

resume_service = ResumeService()

@router.post("/extract")
async def extract_resume(file: UploadFile):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are allowed.")
    
    response_data = await resume_service.extract_resume(file)

    return {
        "statusCode": 200, 
        "statusMessage": "Extracted data from file successfully.", 
        "data": response_data
    }
