from openai import OpenAI
from ..utils.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def text_to_speech(text: str) -> bytes:
    """
    Преобразование текста в речь с помощью OpenAI TTS.
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="alloy",
            input=text
        )
        return response.content
    except Exception as e:
        raise Exception(f"Ошибка преобразования текста в речь: {str(e)}")

async def generate_voice_response(text: str) -> bytes:
    """
    Генерация голосового ответа для Twilio.
    """
    try:
        return await text_to_speech(text)
    except Exception as e:
        raise Exception(f"Ошибка генерации голосового ответа: {str(e)}")
