#main.py
import os, shutil
from typing import List,cast
from fastapi import FastAPI, Depends, HTTPException, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import LoginRequest, LoginResponse, UserPublic, UserResponse
from security import hash_password, verify_password
from auth import create_access_token, create_refresh_token, decode_token
from fastapi.security import OAuth2PasswordBearer

app = FastAPI(title="FastAPI User Management")

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- REGISTER ----------------
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
    if not phone.isdigit() or len(phone) != 10:
        raise HTTPException(400, "Phone must be 10 digits")

    if db.query(User).filter(User.email == email).first():
        raise HTTPException(400, "Email already exists")

    if db.query(User).filter(User.phone == int(phone)).first():
        raise HTTPException(400, "Phone already exists")

    filename = None
    if dp:
        filename = f"{email}_{dp.filename}"
        with open(f"{MEDIA_DIR}/{filename}", "wb") as f:
            shutil.copyfileobj(dp.file, f)

    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=int(phone),
        address=address,
        dp=f"/media/{filename}" if filename else "",
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ---------------- LOGIN ----------------
@app.post("/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not verify_password(data.password, cast(str,user.password)):
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token(cast(int,user.id)),
        "refresh_token": create_refresh_token(cast(int,user.id)),
        "user": user,
    }

# ---------------- GET ALL USERS ----------------
@app.get("/users", response_model=List[UserPublic])
def get_users(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    decode_token(token)
    user = db.query(User).all()
    return user

# ---------------- GET CURRENT USER ----------------
@app.get("/users/me", response_model=UserPublic)
def get_me(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    user_id = decode_token(token)
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    return user
