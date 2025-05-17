   #!/bin/zsh

   # Активируем виртуальное окружение
   source venv/bin/activate

   # Запускаем сервер FastAPI в фоне
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &

   # Запускаем cloudflared tunnel (замени <имя_туннеля> на своё)
   cloudflared tunnel run voice-servis &

   # Ждём завершения обоих процессов
   wait
