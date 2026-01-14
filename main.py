import os
import shutil
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from schemas import UserResponse
from security import hash_password

app = FastAPI()

MEDIA_DIR = "media"
os.makedirs(MEDIA_DIR, exist_ok=True)

# Serve media files
app.mount("/media", StaticFiles(directory=MEDIA_DIR), name="media")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users", response_model=UserResponse)
async def create_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    address: str | None = Form(None),
    dp: UploadFile | None = File(None),
    db: Session = Depends(get_db)
):
    # Check email
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    # Check phone
    if db.query(User).filter(User.phone == phone).first():
        raise HTTPException(status_code=400, detail="Phone already registered")

    dp_path = None

    # Save image
    if dp:
        if dp.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(status_code=400, detail="Only JPG/PNG allowed")

        filename = f"{email}_{dp.filename}"
        dp_path = os.path.join(MEDIA_DIR, filename)

        with open(dp_path, "wb") as buffer:
            shutil.copyfileobj(dp.file, buffer)

        # Change dp_path to URL
        dp_url = f"/media/{filename}"
    else:
        dp_url = None

    new_user = User(
        name=name,
        email=email,
        password=hash_password(password),
        phone=phone,
        address=address,
        dp=dp_url
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
