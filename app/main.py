from fastapi import FastAPI
from routers import resume_router

app = FastAPI()

app.include_router(resume_router)

@app.get("/")
async def root():
    return {"message": "Resume Extraction Service is Healthy!"}
