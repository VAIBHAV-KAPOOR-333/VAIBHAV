#security.py
import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _pre_hash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def hash_password(password: str) -> str:
    return pwd_context.hash(_pre_hash(password))

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(_pre_hash(plain), hashed)

