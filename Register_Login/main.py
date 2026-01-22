"""
main.py
-------
FastAPI application for user registration, login, password reset, and serving user info.
"""

import os
import shutil
import random
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from typing import List

from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from database import SessionLocal, Base, engine
from models import User
from schemas import (
    LoginRequest, LoginResponse,
    UserPublic, UserResponse,
    ForgotPasswordRequest, ResetPasswordRequest
)
from security import hash_password, verify_password
from auth import create_access_token, create_refresh_token, decode_token

# Load environment variables from .env file
load_dotenv()

# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------
SMTP_HOST = os.getenv("SMTP_HOST")
SMTP_PORT = int(os.getenv("SMTP_PORT") or 0)
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
FROM_EMAIL = os.getenv("FROM_EMAIL")

# -----------------------------
# CREATE DATABASE TABLES (optional, Alembic preferred)
# -----------------------------
# Base.metadata.create_all(bind=engine)

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="FastAPI User Management")

# Serve profile images via /media URL
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# OAuth2 dependency to read token from requests
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -----------------------------
# In-memory OTP storage for password reset
# -----------------------------
OTP_STORE: dict[str, str] = {}

# -----------------------------
# DATABASE SESSION DEPENDENCY
# -----------------------------
def get_db():
    """Provide a database session to FastAPI endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -----------------------------
# HELPER FUNCTION TO SEND EMAIL
# -----------------------------
def send_email(to_email: str, subject: str, body: str):
    """
    Send an email using SMTP.
    """
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
# REGISTER NEW USER
# -----------------------------
@app.post("/register", response_model=UserResponse)
async def register(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    dp: UploadFile | None = File(None),
    db: Session = Depends(get_db),
):
    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already exists")

    # Save profile picture
    filename = None
    if dp:
        filename = f"{email}_{dp.filename}"
        with open(f"{MEDIA_DIR}/{filename}", "wb") as f:
            shutil.copyfileobj(dp.file, f)

    # Create user
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=str(phone),
        address=address,
        dp=f"/media/{filename}" if filename else "",
    )

    # Save user to DB
    db.add(user)
    db.commit()
    db.refresh(user)

    # Send welcome email (non-blocking if fails)
    send_email(email, "Welcome!", f"Hi {name}, welcome to our app!")

    return user

# -----------------------------
# LOGIN USER
# -----------------------------
@app.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

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
        raise HTTPException(404, "User not found")

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    OTP_STORE[data.email] = otp

    # Send OTP email
    send_email(data.email, "Reset OTP", f"Hi {user.name}, your OTP is {otp}")
    return {"message": "OTP sent"}

# -----------------------------
# RESET PASSWORD
# -----------------------------
@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    if OTP_STORE.get(data.email) != data.otp:
        raise HTTPException(400, "Invalid OTP")

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    user.password = hash_password(data.new_password)
    db.commit()
    OTP_STORE.pop(data.email)
    return {"message": "Password reset successful"}

# -----------------------------
# GET ALL USERS (PROTECTED)
# -----------------------------
@app.get("/users", response_model=List[UserPublic])
def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decode_token(token)  # verify JWT
    return db.query(User).all()
