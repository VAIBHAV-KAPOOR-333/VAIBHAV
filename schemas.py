import re
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator


# =========================
# USER CREATE SCHEMA
# =========================
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str = Field(..., repr=False)
    phone: str
    address: str

    @field_validator("phone")
    @classmethod
    def phone_must_be_10_digits(cls, value: str):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Phone number must be exactly 10 digits")
        return value

    @field_validator("password")
    @classmethod
    def password_must_have_special_char(cls, value: str):
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise ValueError(
                "Password must contain at least one special character"
            )
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return value


# =========================
# USER RESPONSE (DB → API)
# =========================
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    phone: int
    address: str
    dp: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


# =========================
# PUBLIC USER (NO PASSWORD)
# =========================
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


# =========================
# LOGIN REQUEST
# =========================
class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(..., repr=False)  # hidden in Swagger logs


# =========================
# LOGIN RESPONSE
# =========================
class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserPublic
