from fastapi import FastAPI

app = FastAPI()

@app.post("/process")
def process():
    return {"status": "storage process stub"}

@app.get("/health")
def health():
    return {"status": "ok"} 