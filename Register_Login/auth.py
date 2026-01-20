"""
auth.py
-------
Handles JWT creation and validation.
"""

import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError  # type: ignore
from fastapi import HTTPException, status

# Load environment variables
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_access_token(user_id: int):
    """
    Create a short-lived access token (15 minutes).
    """
    print("[JWT] Creating access token for user:", user_id)
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(minutes=15),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(user_id: int):
    """
    Create a long-lived refresh token (7 days).
    """
    print("[JWT] Creating refresh token for user:", user_id)
    payload = {
        "sub": str(user_id),
        "exp": datetime.now(timezone.utc) + timedelta(days=7),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str) -> int:
    """
    Decode JWT and return user ID.
    Raises HTTPException if invalid.
    """
    try:
        print("[JWT] Decoding token")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("[JWT] Token payload:", payload)
        return int(payload["sub"])
    except (JWTError, KeyError) as exc:
        print("[JWT] Invalid token:", exc)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        ) from exc
