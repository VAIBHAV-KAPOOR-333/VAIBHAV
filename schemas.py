# schemas.py
# ----------------------------------------
# Pydantic schemas used for request validation
# and response serialization
# ----------------------------------------

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field


# ----------------------------------------
# Login request body
# ----------------------------------------
class LoginRequest(BaseModel):
    email: EmailStr                  # validates email format
    password: str = Field(..., repr=False)  # hides password in logs


# ----------------------------------------
# Public user fields (safe to expose)
# ----------------------------------------
class UserPublic(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    address: str
    dp: str | None
    is_active: bool

    # Allows SQLAlchemy model -> schema conversion
    class Config:
        from_attributes = True


# ----------------------------------------
# User response after registration
# ----------------------------------------
class UserResponse(UserPublic):
    created_at: datetime


# ----------------------------------------
# Login response body
# ----------------------------------------
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
