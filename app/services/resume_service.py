import tempfile
import os
from fastapi import UploadFile
from pyresparser import ResumeParser

class ResumeService:
    async def extract_resume(self, file: UploadFile) -> dict:
         # Save the uploaded file to a temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(file.file.read())
            temp_file_path = temp_file.name
        print(temp_file_path)
        
        # Extract data from the resume
        data = ResumeParser(temp_file_path).get_extracted_data()

        # Clean up the temporary file
        os.remove(temp_file_path)

        return data
