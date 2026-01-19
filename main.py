# main.py
# ----------------------------------------
# This file is the main entry point of the FastAPI application.
# It defines routes, dependencies, and connects auth, models, and schemas.
# ----------------------------------------

import os, shutil
from typing import List, cast

# FastAPI core imports
from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form,
)

# Used to serve uploaded files (profile pictures)
from fastapi.staticfiles import StaticFiles

# SQLAlchemy DB session
from sqlalchemy.orm import Session

# Local application imports
from database import SessionLocal
from models import User
from schemas import LoginRequest, LoginResponse, UserPublic, UserResponse
from security import hash_password, verify_password
from auth import create_access_token, create_refresh_token, decode_token

# OAuth2 token extractor (reads token from Authorization header)
from fastapi.security import OAuth2PasswordBearer


# ----------------------------------------
# Create FastAPI application
# ----------------------------------------
app = FastAPI(title="FastAPI User Management")


# ----------------------------------------
# Media (profile picture) configuration
# ----------------------------------------
MEDIA_DIR = "media"

# Create media directory if it does not exist
os.makedirs(MEDIA_DIR, exist_ok=True)

# Mount media directory so files can be accessed via /media/*
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


# ----------------------------------------
# OAuth2 configuration
# tokenUrl="login" means Swagger will call /login to get token
# ----------------------------------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# ----------------------------------------
# Database dependency
# Creates a DB session per request
# ----------------------------------------
def get_db():
    db = SessionLocal()
    print("DB session created")
    try:
        yield db
    finally:
        print("DB session closed")
        db.close()


# ========================================
# REGISTER USER
# ========================================
@app.post("/register", response_model=UserResponse)
async def register(
    # Form fields (multipart/form-data)
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),

    # Optional profile picture upload
    dp: UploadFile | None = File(None),

    # Database session
    db: Session = Depends(get_db),
):
    print("Register API called")   # DEBUG
    print("Email:", email)
    print("Phone:", phone)
    
    # Validate phone number (must be 10 digits)
    if not phone.isdigit() or len(phone) != 10:
        raise HTTPException(400, "Phone must be 10 digits")

    # Check if email already exists
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already exists")

    # Check if phone already exists
    if db.query(User).filter(User.phone == int(phone)).first():
        raise HTTPException(400, "Phone already exists")

    # Handle profile picture upload
    filename = None
    if dp:
        print("Uploaded file:", dp.filename)
        filename = f"{email}_{dp.filename}"
        with open(f"{MEDIA_DIR}/{filename}", "wb") as f:
            shutil.copyfileobj(dp.file, f)

    # Create user object
    user = User(
        name=name,
        email=email,
        password=hash_password(password),  # hash password before storing
        phone=int(phone),
        address=address,
        dp=f"/media/{filename}" if filename else "",
    )

    # Save user to database
    db.add(user)
    print("User added to session")
    
    db.commit()
    print("User committed to DB")

    db.refresh(user)

    return user


# ========================================
# LOGIN USER
# ========================================
@app.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    print("Login API called")
    print("Email received:", data.email)
    # Fetch user by email
    user = db.query(User).filter(User.email == data.email).first()

    # Validate credentials
    if not user:
        print("User not found")
        raise HTTPException(401, "Invalid credentials")

    elif not verify_password(data.password, cast(str, user.password)):
        print("Password mismatch")
        raise HTTPException(401, "Invalid credentials")

    # Return access & refresh tokens
    return {
        "access_token": create_access_token(cast(int, user.id)),
        "refresh_token": create_refresh_token(cast(int, user.id)),
        "user": user,
    }


# ========================================
# GET ALL USERS (Protected)
# ========================================
@app.get("/users", response_model=List[UserPublic])
def get_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("Token received:", token[:15], "...")  #print partial token
    
    # Validate JWT token
    decode_token(token)

    # Fetch all users
    user = db.query(User).all()
    return user


# ========================================
# GET CURRENT LOGGED-IN USER (Protected)
# ========================================
@app.get("/users/me", response_model=UserPublic)
def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    print("Token received of the id ",User.id,":", token[:15], "...")  #print partial token
    
    # Decode token and get user ID
    user_id = decode_token(token)

    # Fetch user by ID
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")

    return user
