from openai import OpenAI
from ..utils.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)

async def transcribe_audio(audio_data: bytes) -> str:
    """
    Преобразование речи в текст с помощью Whisper.
    """
    try:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_data,
            language="ru"
        )
        return response.text
    except Exception as e:
        return f"Ошибка распознавания речи: {str(e)}"

async def process_voice_input(audio_url: str) -> str:
    """
    Обработка голосового ввода от Twilio.
    """
    try:
        import requests
        response = requests.get(audio_url)
        if response.status_code == 200:
            return await transcribe_audio(response.content)
        return "Ошибка загрузки аудиофайла"
    except Exception as e:
        return f"Ошибка обработки голосового ввода: {str(e)}"
