from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# phpMyAdmin / MySQL credentials
DATABASE_URL = "wbuser+newpassword123://:127.0.0.1@user_db:3306/fastapi_db"
#               └──user └──pass        └host      └db_name

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
