from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from backend.api.routes.health_routes import router as health_router
from backend.api.routes.user_routes import router as user_router
from backend.db.database import connect_to_db, disconnect_from_db, create_tables

##Observability
#from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Gauge, make_asgi_app


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
#Instrumentator().instrument(app).expose(app)

REQUEST_COUNT = Counter(
    'http_request_count', 'Total HTTP requests', ['method', 'endpoint', 'http_status']
)
IN_PROGRESS = Gauge(
    'inprogress_requests', 'Requests in progress'
)

# Middleware to update metrics per request
@app.middleware("http")
async def prometheus_metrics(request: Request, call_next):
    IN_PROGRESS.inc()
    response = await call_next(request)
    REQUEST_COUNT.labels(
        method=request.method,
        endpoint=request.url.path,
        http_status=response.status_code,
    ).inc()
    IN_PROGRESS.dec()
    return response

# Mount /metrics endpoint
app.mount("/metrics", make_asgi_app())