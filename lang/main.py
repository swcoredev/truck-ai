from fastapi import FastAPI
from pydantic import BaseModel
from langdetect import detect

app = FastAPI()

class TextRequest(BaseModel):
    text: str

@app.post("/process")
def process(request: TextRequest):
    try:
        lang = detect(request.text)
        return {"detected_language": lang}
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"} 