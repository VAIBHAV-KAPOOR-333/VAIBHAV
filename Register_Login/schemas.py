"""
schemas.py
----------
Define request/response models for FastAPI.
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# -------- LOGIN REQUEST --------
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., repr=False)  # Do not show password in logs

# -------- USER RESPONSE --------
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    address: str
    dp: str | None
    is_active: bool

    class Config:
        from_attributes = True  # ORM -> Pydantic conversion

# -------- REGISTER RESPONSE --------
class UserResponse(UserPublic):
    created_at: datetime

# -------- LOGIN RESPONSE --------
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic

# -------- FORGOT PASSWORD REQUEST --------
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# -------- RESET PASSWORD REQUEST --------
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
