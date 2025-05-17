import requests

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

def test_health():
    for name, port in MODULES.items():
        url = f"http://localhost:{port}/health"
        resp = requests.get(url, timeout=2)
        assert resp.status_code == 200, f"{name} not healthy" 