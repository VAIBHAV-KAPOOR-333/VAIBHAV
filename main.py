# main.py
import os
import shutil
from typing import cast

from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    UploadFile,
    File,
    Form
)
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import (
    UserResponse,
    LoginRequest,
    LoginResponse
)
from security import hash_password, verify_password
from auth import create_access_token, create_refresh_token


# --------------------------------------------------
# App setup
# --------------------------------------------------

app = FastAPI(title="FastAPI User Management")

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Serve uploaded images
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


# --------------------------------------------------
# Database dependency
# --------------------------------------------------

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------------------------------------
# Create user (with profile image)
# --------------------------------------------------

@app.post("/users", response_model=UserResponse)
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    address: str = Form(...),
    dp: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # ---------- Phone validation ----------
    if not phone.isdigit() or len(phone) != 10:
        raise HTTPException(
            status_code=400,
            detail="Phone must be exactly 10 digits"
        )

    # ---------- Uniqueness checks ----------
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if db.query(User).filter(User.phone == int(phone)).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    # ---------- Image upload ----------
    dp_url = None
    if dp:
        if dp.content_type not in ("image/jpeg", "image/png"):
            raise HTTPException(
                status_code=400,
                detail="Only JPG or PNG images allowed"
            )

        filename = f"{email}_{dp.filename}"
        file_path = os.path.join(MEDIA_DIR, filename)

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(dp.file, buffer)

        dp_url = f"/media/{filename}"

    # ---------- Create user ----------
    user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=int(phone),
        address=address,
        dp=dp_url
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


# --------------------------------------------------
# Login
# --------------------------------------------------

@app.post("/login", response_model=LoginResponse)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, cast(str, user.password)):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    return {
        "access_token": create_access_token(cast(int, user.id)),
        "refresh_token": create_refresh_token(cast(int, user.id)),
        "token_type": "bearer",
        "user": user
    }
