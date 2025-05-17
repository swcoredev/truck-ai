from fastapi import FastAPI, Request, Response
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
import time

REQUEST_COUNT = Counter('app_requests_total', 'Total number of requests', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('app_request_latency_seconds', 'Request latency', ['endpoint'])
ERROR_COUNT = Counter('app_errors_total', 'Total number of errors', ['endpoint'])

app = FastAPI()

@app.middleware('http')
async def metrics_middleware(request: Request, call_next):
    start_time = time.time()
    try:
        response = await call_next(request)
        REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
        return response
    except Exception as e:
        ERROR_COUNT.labels(request.url.path).inc()
        raise e
    finally:
        resp_time = time.time() - start_time
        REQUEST_LATENCY.labels(request.url.path).observe(resp_time)

@app.get('/metrics')
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST) 