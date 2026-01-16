#schemas.py
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., repr=False)

class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    address: str
    dp: str | None
    is_active: bool

    class Config:
        from_attributes = True

class UserResponse(UserPublic):
    created_at: datetime

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
