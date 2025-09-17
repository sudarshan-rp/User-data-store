from fastapi import FastAPI
from contextlib import asynccontextmanager
from backend.api.routes.health_routes import router as health_router
from backend.api.routes.user_routes import router as user_router
from backend.db.database import connect_to_db, disconnect_from_db, create_tables

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
