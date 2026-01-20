"""
main.py
-------
FastAPI application for user registration, login, and password reset.
"""

import os, shutil, random, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from typing import List, cast

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

# Load .env
load_dotenv()

# -----------------------------
# EMAIL CONFIGURATION
# -----------------------------
SMTP_HOST = os.getenv("SMTP_HOST") or ""
SMTP_PORT = int(os.getenv("SMTP_PORT") or 0)
SMTP_USER = os.getenv("SMTP_USER") or ""
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD") or ""
FROM_EMAIL = os.getenv("FROM_EMAIL") or ""

# -----------------------------
# CREATE DATABASE TABLES
# -----------------------------
Base.metadata.create_all(bind=engine)
print("[DB] Tables created if not exist")

# -----------------------------
# FASTAPI APP
# -----------------------------
app = FastAPI(title="FastAPI User Management")

# Serve profile images via /media/*
MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

# OAuth2 token reader
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# -----------------------------
# OTP STORE (IN MEMORY)
# -----------------------------
OTP_STORE: dict[str, str] = {}

# -----------------------------
# DATABASE DEPENDENCY
# -----------------------------
def get_db():
    print("[DB] Opening DB session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        print("[DB] DB session closed")

# -----------------------------
# EMAIL FUNCTION
# -----------------------------
def send_email(to_email: str, subject: str, body: str):
    """
    Send email using SMTP.
    Wrap in try/except to prevent crashes if network fails.
    """
    print("[EMAIL] Sending email to:", to_email)
    msg = EmailMessage()
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print("[EMAIL] Email sent successfully")
    except (smtplib.SMTPException, OSError) as e:  # type: ignore
        print("[EMAIL ERROR] Could not send email:", e)

# -----------------------------
# REGISTER USER
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
    print("[REGISTER] API called for:", email)

    # Check if user already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already exists")

    # Save profile image if provided
    filename = None
    if dp:
        print("[REGISTER] Saving profile image:", dp.filename)
        filename = f"{email}_{dp.filename}"
        with open(f"{MEDIA_DIR}/{filename}", "wb") as f:
            shutil.copyfileobj(dp.file, f)

    # Create user object
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=str(phone),
        address=address,
        dp=f"/media/{filename}" if filename else "",
    )

    # Save to database
    db.add(user)
    db.commit()
    db.refresh(user)
    print("[REGISTER] User saved to DB:", user.email)

    # Send welcome email (will not crash API if fails)
    send_email(email, "Welcome to FastAPI", f"Hi {name},\n\nWelcome to our app!")

    return user

# -----------------------------
# LOGIN
# -----------------------------
@app.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    print("[LOGIN] Attempt:", data.email)

    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, cast(str, user.password)):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token(cast(int, user.id)),
        "refresh_token": create_refresh_token(cast(int, user.id)),
        "user": user,
    }

# -----------------------------
# FORGOT PASSWORD
# -----------------------------
@app.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    print("[FORGOT] Request for:", data.email)

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")

    # Generate OTP
    otp = str(random.randint(100000, 999999))
    OTP_STORE[data.email] = otp
    print("[FORGOT] OTP generated:", otp)

    # Send OTP via email
    send_email(data.email, "Password Reset OTP", f"Hi {user.name},\nYour OTP is: {otp}")

    return {"message": "OTP sent"}

# -----------------------------
# RESET PASSWORD
# -----------------------------
@app.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    print("[RESET] Attempt for:", data.email)

    if OTP_STORE.get(data.email) != data.otp:
        raise HTTPException(400, "Invalid OTP")

    user = db.query(User).filter(User.email == data.email).first()
    if not user:
        raise HTTPException(404, "User not found")
    
    hashed_pwd = hash_password(data.new_password)
    user.password = hashed_pwd  # type: ignore
    db.commit()
    OTP_STORE.pop(data.email)
    print("[RESET] Password reset successful for:", data.email)

    return {"message": "Password reset successful"}

# -----------------------------
# GET USERS (PROTECTED)
# -----------------------------
@app.get("/users", response_model=List[UserPublic])
def get_users(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    decode_token(token)
    all_users = db.query(User).all()
    print("[USERS] Returning", len(all_users), "users")
    return all_users
