# database.py
# ----------------------------------------
# Database engine & session setup
# ----------------------------------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# MySQL database URL
DATABASE_URL = "mysql+pymysql://wbuser:newpassword123@127.0.0.1:3306/fastapi_db"


# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Create DB session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()
