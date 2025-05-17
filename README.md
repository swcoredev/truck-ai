# TruckAI — Универсальный микросервисный голосовой каркас

## Назначение
TruckAI — это универсальный шаблон для построения голосовых и AI-систем на базе микросервисов.
- Основа на FastAPI
- Лёгкая интеграция с Twilio, GPT, Whisper, TTS и другими AI-инструментами
- Подходит для любых сфер: сервисы, отели, техподдержка, автоматизация, контакт-центры и др.

---

## Архитектура
- Микросервисная: каждый модуль — отдельный сервис, общение только по HTTP API
- Независимый запуск каждого модуля
- Поддержка Dev Mode для отладки
- Развёртывание вручную или через Docker Compose

---

## Модули
| Модуль         | Назначение |
|---------------|------------|
| **call_handler** | Приём входящих событий (например, звонков), запуск цепочки обработки |
| **gpt**          | Генерация текста через OpenAI GPT или аналогичные AI-сервисы |
| **stt**          | Распознавание речи (аудио в текст, Whisper и др.) |
| **tts**          | Синтез речи (текст в аудио, ElevenLabs, Google TTS и др.) |
| **lang**         | Определение языка текста, переключение языков |
| **lead_sender**  | Сохранение/отправка структурированных заявок (email, Telegram, БД) |
| **gateway**      | Центральный API-шлюз, маршрутизация запросов между модулями |
| **monitoring**   | Метрики, интеграция с Prometheus, endpoint /metrics |
| **logger**       | Логирование действий, ошибок, сессий |
| **admin_panel**  | Веб-интерфейс администратора (заглушка) |
| **config**       | Глобальные настройки, шаблоны .env |
| **storage**      | Хранение файлов, аудио, логов |
| **healthcheck**  | Скрипты проверки статуса сервисов |
| **tests**        | Автотесты для всех модулей |

---

## Структура проекта
```
voice-block/
├── call_handler/
├── gpt/
├── stt/
├── tts/
├── lang/
├── lead_sender/
├── gateway/
├── monitoring/
├── logger/
├── admin_panel/
├── config/
├── storage/
├── healthcheck/
├── tests/
├── docs/
├── docker-compose.yml
├── README.md
├── .github/
│   └── workflows/
│       └── test.yml
```

---

## Установка и запуск

1. **В каждом модуле:**
   ```bash
   cd <module_name>
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port <порт>
   ```
   Пример: для stt — порт 8001, для tts — 8004 и т.д.

2. **Запуск всех сервисов через Docker Compose:**
   ```bash
   docker-compose up --build
   ```

---

## Переменные окружения (.env)

**Ключевые переменные:**
- IS_DEV=true                # Включить режим разработчика
- OPENAI_API_KEY=...         # Ключ для OpenAI
- TWILIO_ACCOUNT_SID=...     # SID для Twilio
- TWILIO_AUTH_TOKEN=...      # Токен для Twilio
- TWILIO_PHONE_NUMBER=...    # Телефон Twilio
- PORT=8001                  # Порт сервиса
- API_URL=http://...         # URL других сервисов

**Пример .env:**
```
IS_DEV=true
OPENAI_API_KEY=sk-xxx
TWILIO_ACCOUNT_SID=ACxxx
TWILIO_AUTH_TOKEN=xxx
TWILIO_PHONE_NUMBER=+1234567890
PORT=8001
API_URL=http://localhost:8002
```

---

## Примеры API-запросов

### GPT (Text Generation)
```bash
curl -X POST http://localhost:8003/process -H "Content-Type: application/json" -d '{"user_input": "Привет, как дела?"}'
```

### STT (Speech-to-Text)
```bash
curl -X POST http://localhost:8001/process -H "Content-Type: application/json" -d '{"audio_url": "test.mp3"}'
```

### TTS (Text-to-Speech)
```bash
curl -X POST http://localhost:8004/process -H "Content-Type: application/json" -d '{"text": "Привет, как дела?"}' --output output.mp3
```

### Lead Sender (Сохранение заявки)
```bash
curl -X POST http://localhost:8005/process -H "Content-Type: application/json" -d '{"name": "Иван", "phone": "+79991234567", "city": "Москва", "dates": "01.07 — 10.07"}'
```

---

## Monitoring
- В каждом сервисе реализован endpoint `/metrics` для Prometheus-метрик (время ответа, статус, ошибки)
- Пример интеграции — monitoring/metrics.py
- Можно подключить Prometheus для сбора и визуализации метрик

---

## CI/CD
- В проекте настроен автозапуск тестов через GitHub Actions: `.github/workflows/test.yml`
- Все тесты из папки `tests/` запускаются автоматически при каждом push и pull request

---

## Как добавить новый модуль
1. Скопируйте шаблон любого существующего модуля
2. Добавьте main.py, requirements.txt, README.md, VERSION.txt, config/
3. Реализуйте endpoint `/process` и `/health`
4. Поддержите Dev Mode через IS_DEV
5. Добавьте Dockerfile и .env.example

---

## Документация
- Архитектура и примеры — в папке `docs/`
- Вопросы и предложения — через Issues на GitHub
