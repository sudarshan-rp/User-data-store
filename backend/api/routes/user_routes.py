from fastapi import APIRouter, Depends, HTTPException
from backend.models.user import UserCreate, UserRead
from backend.services.user_service import UserService

router = APIRouter()

# Dependency
def get_user_service():
    return UserService()

@router.post("/users", response_model=UserRead, tags=["Users"])
async def create_user_endpoint(user: UserCreate, service: UserService = Depends(get_user_service)):
    return await service.create_user(user)

@router.get("/users/{user_id}", response_model=UserRead, tags=["Users"])
async def get_user_endpoint(user_id: int, service: UserService = Depends(get_user_service)):
    user = await service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users", response_model=list[UserRead], tags=["Users"])
async def list_users_endpoint(service: UserService = Depends(get_user_service)):
    return await service.list_users()
