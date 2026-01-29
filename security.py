# security.py
from passlib.context import CryptContext

# Create a password hashing context
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plain password"""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """Verify a password against hash"""
    return pwd_context.verify(plain, hashed)
