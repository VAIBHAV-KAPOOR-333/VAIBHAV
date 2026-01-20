"""
security.py
-----------
Handles password hashing and verification using Argon2.
"""

from passlib.context import CryptContext

### Create password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash a plain-text password using Argon2.
    """
    print("[SECURITY] Hashing password:", password)
    hashed = pwd_context.hash(password)
    print("[SECURITY] Password hashed successfully")
    return hashed

def verify_password(plain: str, hashed: str) -> bool:
    """
    Verify a password during login.
    """
    print("[SECURITY] Verifying password")
    return pwd_context.verify(plain, hashed)
