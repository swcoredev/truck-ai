from fastapi import FastAPI
from .routers import voice
from .utils.config import settings

app = FastAPI(title="Voice Block API")

# Подключаем роутеры
app.include_router(voice.router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )
