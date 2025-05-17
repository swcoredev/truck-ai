from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

app = FastAPI()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

class UserInputRequest(BaseModel):
    user_input: str

async def process_user_request(user_input: str) -> str:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Вы — вежливый голосовой помощник. Всегда отвечайте только на русском языке, даже если вопрос задан на другом языке. Никогда не используйте английский язык в ответах. Отвечайте кратко и по существу."
                },
                {"role": "user", "content": user_input}
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Извините, произошла ошибка: {str(e)}"

@app.post("/process")
async def process(request: UserInputRequest):
    text = await process_user_request(request.user_input)
    return {"response": text}

@app.get("/health")
def health():
    return {"status": "ok"} 