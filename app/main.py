from pyresparser import ResumeParser

from fastapi import FastAPI

app = FastAPI()

@app.get("/resume/extract")
def read_root():
    return read_doc()

def read_doc():
    data = ResumeParser("C:/Users/ASUS/OneDrive/Desktop/senior-project/resume-extraction/src/resume-sample.pdf").get_extracted_data()
    return data




