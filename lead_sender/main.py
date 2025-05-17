from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

class LeadRequest(BaseModel):
    name: str
    phone: str
    city: str
    dates: str

LEADS_FILE = "leads.json"

@app.post("/process")
def process(request: LeadRequest):
    lead = request.dict()
    leads = []
    if os.path.exists(LEADS_FILE):
        with open(LEADS_FILE, "r", encoding="utf-8") as f:
            try:
                leads = json.load(f)
            except Exception:
                leads = []
    leads.append(lead)
    with open(LEADS_FILE, "w", encoding="utf-8") as f:
        json.dump(leads, f, ensure_ascii=False, indent=2)
    return {"status": "lead saved", "lead": lead}

@app.get("/health")
def health():
    return {"status": "ok"} 