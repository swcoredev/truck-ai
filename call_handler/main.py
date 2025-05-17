from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

# Для теста можно использовать локальные адреса, если сервисы запущены на разных портах
STT_URL = "http://localhost:8001/process"
LANG_URL = "http://localhost:8002/process"
GPT_URL = "http://localhost:8003/process"
TTS_URL = "http://localhost:8004/process"
LEAD_URL = "http://localhost:8005/process"

class CallRequest(BaseModel):
    audio_url: str = "test.mp3"
    name: str = "Иван"
    phone: str = "+79991234567"
    city: str = "Ялта"
    dates: str = "01.07 — 10.07"

@app.post("/process")
def process(request: CallRequest):
    results = {}
    # 1. STT
    stt_resp = requests.post(STT_URL, json={"audio_url": request.audio_url})
    stt_text = stt_resp.json().get("text", "")
    results["stt"] = stt_text
    # 2. LANG
    lang_resp = requests.post(LANG_URL, json={"text": stt_text})
    lang = lang_resp.json().get("detected_language", "unknown")
    results["lang"] = lang
    # 3. GPT
    gpt_resp = requests.post(GPT_URL, json={"user_input": stt_text})
    gpt_answer = gpt_resp.json().get("response", "")
    results["gpt"] = gpt_answer
    # 4. TTS
    tts_resp = requests.post(TTS_URL, json={"text": gpt_answer})
    results["tts_audio_status"] = "ok" if tts_resp.status_code == 200 else "error"
    # 5. LEAD
    lead_payload = {
        "name": request.name,
        "phone": request.phone,
        "city": request.city,
        "dates": request.dates
    }
    lead_resp = requests.post(LEAD_URL, json=lead_payload)
    results["lead_sender"] = lead_resp.json()
    return results

@app.get("/health")
def health():
    return {"status": "ok"} 