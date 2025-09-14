from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    
class UserRead(BaseModel):
    id: Optional[int]
    name: str
    email: EmailStr
