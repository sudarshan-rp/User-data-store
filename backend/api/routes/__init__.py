from fastapi import APIRouter
from backend.api.routes import health_routes, user_routes




router = APIRouter()
router.include_router(health_routes.router, tags=["Health"])
router.include_router(user_routes.router, tags=["Users"])
