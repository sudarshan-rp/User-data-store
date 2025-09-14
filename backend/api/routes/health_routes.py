# backend/api/routes.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Backend API is healthy 🚀"}
