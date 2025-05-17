from fastapi import FastAPI

app = FastAPI()

@app.post("/process")
def process():
    return {"status": "gateway process stub"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/status")
def status():
    return {"status": "gateway running", "version": "v0.1.0"} 