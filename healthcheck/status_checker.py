import requests
import time

MODULES = {
    "stt": 8001,
    "lang": 8002,
    "gpt": 8003,
    "tts": 8004,
    "lead_sender": 8005,
    "call_handler": 8006,
    "logger": 8007,
    "storage": 8008
}

for name, port in MODULES.items():
    url = f"http://localhost:{port}/health"
    try:
        resp = requests.get(url, timeout=2)
        if resp.status_code == 200:
            print(f"{name}: OK")
        else:
            print(f"{name}: ERROR (status {resp.status_code})")
    except Exception as e:
        print(f"{name}: NO RESPONSE ({e})") 