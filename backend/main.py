from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from backend.api.routes.health_routes import router as health_router
from backend.api.routes.user_routes import router as user_router
from backend.db.database import connect_to_db, disconnect_from_db, create_tables

##Observability
from prometheus_client import Counter, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi.responses import Response


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await connect_to_db()
    await create_tables()
    yield
    # Shutdown
    await disconnect_from_db()

def create_app() -> FastAPI:
    app = FastAPI(
        title="User Data Store",
        version="1.0.0",
        description="Backend API for manageing user data",
        lifespan=lifespan 
    )

    # Include API routes
    app.include_router(health_router, prefix="/api")
    app.include_router(user_router, prefix="/users")

    return app

app = create_app()


#---------------------------- Observability ---------------------------
REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status_code']
)
IN_PROGRESS = Gauge(
    'http_requests_in_progress', 'HTTP requests currently being processed'
)

# Middleware to update metrics per request
@app.middleware("http")
async def prometheus_metrics(request: Request, call_next):
    IN_PROGRESS.inc()
    try:
        response = await call_next(request)
        REQUEST_COUNT.labels(
            method=request.method,
            endpoint=request.url.path,
            status_code=response.status_code,
        ).inc()
        return response
    finally:
        IN_PROGRESS.dec()

# Metrics endpoint
@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)