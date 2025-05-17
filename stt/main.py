from fastapi import FastAPI, Request
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import requests
from openai import OpenAI
from utils_dev import dev_log, timed_action, IS_DEV
import time

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class AudioUrlRequest(BaseModel):
    audio_url: str

async def transcribe_audio(audio_data: bytes) -> str:
    def _transcribe():
        try:
            client = OpenAI(api_key=OPENAI_API_KEY)
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_data,
                language="ru"
            )
            dev_log(f"Whisper ответ: {response.text}")
            return response.text
        except Exception as e:
            dev_log(f"Ошибка распознавания речи: {str(e)}")
            return f"Ошибка распознавания речи: {str(e)}"
    return timed_action("Распознавание речи", _transcribe)

@app.post("/process")
async def process(request: AudioUrlRequest):
    dev_log(f"Получен audio_url: {request.audio_url}")
    if IS_DEV and request.audio_url == "test.mp3":
        dev_log("Симуляция STT: возвращаем 'Тестовая фраза'")
        return {"text": "Тестовая фраза (Dev Mode)"}
    try:
        response = requests.get(request.audio_url)
        if response.status_code == 200:
            text = await transcribe_audio(response.content)
            return {"text": text}
        dev_log("Ошибка загрузки аудиофайла")
        return {"error": "Ошибка загрузки аудиофайла"}
    except Exception as e:
        dev_log(f"Ошибка обработки голосового ввода: {str(e)}")
        return {"error": f"Ошибка обработки голосового ввода: {str(e)}"}

@app.get("/health")
def health():
    return {"status": "ok"} 