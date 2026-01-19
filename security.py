# security.py
# ----------------------------------------
# Handles password hashing & verification
# ----------------------------------------

import hashlib
from passlib.context import CryptContext


# Configure bcrypt hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ----------------------------------------
# Pre-hash password using SHA-256
# (extra security layer)
# ----------------------------------------
def _pre_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


# ----------------------------------------
# Hash password for storage
# ----------------------------------------
def hash_password(password: str) -> str:
    return pwd_context.hash(_pre_hash(password))


# ----------------------------------------
# Verify password during login
# ----------------------------------------
def verify_password(plain: str, hashed: str) -> bool:
    print("Verifying password")
    return pwd_context.verify(_pre_hash(plain), hashed)
