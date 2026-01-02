from pydantic import BaseModel, field_validator


class RegisterCreate(BaseModel):
id: int
name: str
phone: int
address: str


@field_validator("phone")
@classmethod
def validate_phone(cls, v):
phone_str = str(v)
if not phone_str.isdigit() or len(phone_str) != 10:
raise ValueError("Phone number must be exactly 10 digits")
return v


class RegisterResponse(BaseModel):
id: int
name: str
phone: int
address: str


class Config:
from_attributes = True