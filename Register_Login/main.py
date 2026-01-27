"""
main.py
-------
FastAPI app with registration, login, password reset, and protected users route.
"""

import os
import shutil
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from typing import List, Dict

from fastapi import (
    FastAPI, Depends, HTTPException,
    UploadFile, File, Form, status
)
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from database import SessionLocal
from models import User
from schemas import (
    LoginRequest, LoginResponse,
    UserPublic, UserResponse,
    ForgotPasswordRequest, ResetPasswordRequest
)
from security import hash_password, verify_password
from auth import create_access_token, create_refresh_token, decode_token

load_dotenv()

# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="FastAPI User Management")

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# OTP store (in-memory)
OTP_STORE: Dict[str, str] = {}

# -----------------------------
# DB DEPENDENCY
# -----------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# EMAIL HELPER (NON-BLOCKING SAFE)
# -----------------------------
def send_email(to_email: str, subject: str, body: str):
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD, FROM_EMAIL]):
        print("[EMAIL ERROR] SMTP not configured")
        return

    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print("[EMAIL ERROR]", e)

# -----------------------------
# ROUTES
# -----------------------------

@app.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    dp: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    # Pre-check email
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=409, detail="Email already exists")

    filename = None
    if dp:
        filename = f"{email}_{dp.filename}"
        file_path = os.path.join(MEDIA_DIR, filename)
        with open(file_path, "wb") as f:
            shutil.copyfileobj(dp.file, f)

    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=str(phone),
        address=address,
        dp=f"/media/{filename}" if filename else "",
        is_active=1,
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email or phone number already exists"
        )

    # Email must NEVER break registration
    send_email(email, "Welcome!", f"Hi {name}, welcome to our app!")

    return user

# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
        "user": user,
    }

# -----------------------------
# FORGOT PASSWORD
# -----------------------------
@app.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp = str(random.randint(100000, 999999))
    OTP_STORE[data.email] = otp

    send_email(
        data.email,
        "Password Reset OTP",
        f"Hi {user.name}, your OTP is {otp}"
    )

    return {"message": "OTP sent successfully"}

# -----------------------------
# RESET PASSWORD
# -----------------------------
@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    stored_otp = OTP_STORE.get(data.email)

    if not stored_otp or stored_otp != data.otp:
        raise HTTPException(status_code=400, detail="Invalid or expired OTP")

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(data.new_password)
    db.commit()

    OTP_STORE.pop(data.email, None)

    return {"message": "Password reset successful"}

# -----------------------------
# PROTECTED ROUTE
# -----------------------------
@app.get("/users", response_model=List[UserPublic])
def get_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    decode_token(token)
    users=db.query(User).all()
    return users
