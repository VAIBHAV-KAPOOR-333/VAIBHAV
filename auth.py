# auth.py
# ----------------------------------------
# Handles JWT access & refresh tokens
# ----------------------------------------

from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer


# ----------------------------------------
# JWT configuration
# ----------------------------------------
SECRET_KEY = "SUPER_SECRET_KEY_CHANGE_ME"
ALGORITHM = "HS256"


# Used by Swagger & Depends() to read Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ----------------------------------------
# Create short-lived access token
# ----------------------------------------
def create_access_token(user_id: int):
    print("Creating access token for user:", user_id)
    payload = {
        "sub": str(user_id),  # subject = user ID
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------------------
# Create long-lived refresh token
# ----------------------------------------
def create_refresh_token(user_id: int):
    print("Creating refresh token for user:", user_id)
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


# ----------------------------------------
# Decode & validate JWT token
# ----------------------------------------
def decode_token(token: str) -> int:
    try:
        print("Decoding token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) 
        print("Token payload:", payload)
        return int(payload["sub"])
    except (JWTError, KeyError) as exc:
        print("Token decode failed:", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc
