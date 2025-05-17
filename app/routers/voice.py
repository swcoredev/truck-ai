from fastapi import APIRouter, Request, Response
from twilio.twiml.voice_response import VoiceResponse
from ..services.stt import process_voice_input
from ..services.gpt_handler import process_user_request, extract_intent
from ..services.tts import generate_voice_response
import requests
from ..utils.config import settings

router = APIRouter()

@router.post("/voice")
async def handle_voice(request: Request):
    """
    Обработка входящих голосовых вызовов от Twilio.
    """
    form_data = await request.form()
    response = VoiceResponse()
    
    # Проверяем, новый ли это звонок или ответ на пользовательский ввод
    if "SpeechResult" in form_data:
        # Обрабатываем речевой ввод пользователя
        user_input = form_data["SpeechResult"]
        print(f"SpeechResult: {user_input}")
        
        # Обрабатываем через GPT
        gpt_response = await process_user_request(user_input)
        print(f"GPT response: {gpt_response}")
        
        # Извлекаем намерение для Servis.Work
        # intent_data = await extract_intent(user_input)
        # Отправляем в Servis.Work API
        # try:
        #     requests.post(
        #         settings.SERVIS_WORK_API_URL,
        #         json=intent_data,
        #         headers={"Authorization": f"Bearer {settings.SERVIS_WORK_API_KEY}"}
        #     )
        # except Exception as e:
        #     print(f"Ошибка отправки в Servis.Work: {str(e)}")
        
        # Генерируем голосовой ответ
        response.say(gpt_response, voice="Polly.Tatyana", language="ru-RU")
    else:
        # Начальное приветствие
        welcome_message = "Здравствуйте! Это компания Servis Work, менеджер по продажам Светлана Сергеевна на связи. Чем могу помочь вам сегодня?"
        response.say(welcome_message, voice="Polly.Tatyana", language="ru-RU")
        response.gather(input="speech", action="/api/v1/voice", method="POST", language="ru-RU")
    
    return Response(content=str(response), media_type="application/xml")
