# schemas.py
import re
from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime

class UserCreate(BaseModel):
    name: str = Field(..., example="Vaibhav")
    email: EmailStr = Field(..., example="vaibhav@gmail.com")
    password: str = Field(..., example="Password@123")
    phone: str = Field(..., example="9876543210")
    address: str | None = Field(None, example="Bangalore, India")

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
            raise ValueError("Password must contain at least one special character")
        return value


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    address: str | None
    dp: str | None
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True
