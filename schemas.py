from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

# Request for login
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., repr=False)

# Public user info (hide sensitive fields)
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: str
    address: str
    dp: str | None
    is_active: bool

    class Config:
        from_attributes = True  # Convert SQLAlchemy objects to Pydantic

# Response after registering a user
class UserResponse(UserPublic):
    created_at: datetime

# Response after login
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic

# Request to send OTP for password reset
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

# Request to reset password using OTP
class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str
