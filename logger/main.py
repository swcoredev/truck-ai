from fastapi import FastAPI

app = FastAPI()

@app.post("/process")
def process():
    return {"status": "logger process stub"}

@app.get("/health")
def health():
    return {"status": "ok"} 