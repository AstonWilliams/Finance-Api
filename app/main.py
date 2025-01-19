from fastapi import FastAPI, Request, Response
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from contextlib import asynccontextmanager
from app.routers import news, yahoo_finance
from app.db.database import Base, engine
from app.services.news import continuous_fetch
from app.services.yahoo_finance import continuous_yahoo_finance_fetch
import time
import asyncio
import psutil

# Prometheus metrics
REQUEST_COUNT = Counter("request_count_total", "Total number of requests", ["method", "endpoint"])
REQUEST_LATENCY = Histogram("request_latency_seconds", "Request latency in seconds", ["method", "endpoint"])
ERROR_COUNT = Counter("error_count_total", "Total number of errors", ["method", "endpoint"])

# Create the database tables
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Start background tasks
    task_news = asyncio.create_task(continuous_fetch())
    task_yahoo_finance = asyncio.create_task(continuous_yahoo_finance_fetch())
    yield
    task_news.cancel()
    task_yahoo_finance.cancel()

app = FastAPI(lifespan=lifespan)

app.include_router(news.router)
app.include_router(yahoo_finance.router)

@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    request_latency = time.time() - start_time

    REQUEST_COUNT.labels(method=request.method, endpoint=request.url.path).inc()
    REQUEST_LATENCY.labels(method=request.method, endpoint=request.url.path).observe(request_latency)
    
    if response.status_code >= 400:
        ERROR_COUNT.labels(method=request.method, endpoint=request.url.path).inc()

    return response

@app.get("/metrics")
def metrics():
    # Generate metrics data
    metrics_data = generate_latest()
    return Response(metrics_data, media_type=CONTENT_TYPE_LATEST)

@app.get("/metrics_json")
def metrics_json():
    metrics_data = generate_latest().decode('utf-8')
    metrics_lines = metrics_data.split('\n')
    
    metrics_dict = {}
    for line in metrics_lines:
        if not line.startswith('#') and line:
            key, value = line.split(' ', 1)
            metrics_dict[key] = value

    return JSONResponse(content=metrics_dict)

@app.get("/health")
def health_check():
    # Extract metric values
    request_count = sum(sample.value for sample in REQUEST_COUNT.collect()[0].samples if sample.name == 'request_count_total')
    error_count = sum(sample.value for sample in ERROR_COUNT.collect()[0].samples if sample.name == 'error_count_total')
    latency_sum = sum(sample.value for sample in REQUEST_LATENCY.collect()[0].samples if sample.name.endswith('_sum'))
    latency_count = sum(sample.value for sample in REQUEST_LATENCY.collect()[0].samples if sample.name.endswith('_count'))
    average_latency = latency_sum / latency_count if latency_count > 0 else 0

    # Define thresholds
    max_error_rate = 0.05
    max_average_latency = 1.0
    error_rate = error_count / request_count if request_count else 0
    if error_rate > max_error_rate or average_latency > max_average_latency:
        status = "unhealthy"
    else:
        status = "healthy"

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    return JSONResponse(content={
        "status": status,
        "request_count": request_count,
        "error_count": error_count,
        "error_rate": error_rate,
        "average_latency_seconds": average_latency,
        "cpu_usage_percent": cpu_usage,
        "memory_usage_percent": memory_usage
    })
