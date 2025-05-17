from fastapi import FastAPI, Response
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class TTSRequest(BaseModel):
    text: str

async def text_to_speech(text: str) -> bytes:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content
    except Exception as e:
        raise Exception(f"Ошибка преобразования текста в речь: {str(e)}")

@app.post("/process")
async def process(request: TTSRequest):
    try:
        audio = await text_to_speech(request.text)
        return Response(content=audio, media_type="audio/mpeg")
    except Exception as e:
        return {"error": str(e)}

@app.get("/health")
def health():
    return {"status": "ok"} 