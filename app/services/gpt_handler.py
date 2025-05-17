from openai import OpenAI
from ..utils.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def process_user_request(user_input: str) -> str:
    """
    Обработка запроса пользователя через GPT.
    """
    try:
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

async def extract_intent(user_input: str) -> dict:
    """
    Извлечение намерения и информации из запроса пользователя.
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "Извлеките основное намерение и ключевую информацию из запроса пользователя. Верните JSON с полями: intent, details, priority."
                },
                {"role": "user", "content": user_input}
            ],
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content
    except Exception as e:
        return {"error": str(e)}
