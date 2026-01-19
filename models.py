# models.py
# ----------------------------------------
# SQLAlchemy ORM models
# ----------------------------------------

from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from database import Base


class User(Base):
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True)

    # User details
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    dp = Column(String(255), nullable=False)

    # User status
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps (handled by MySQL)
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
    updated_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        nullable=False,
    )
