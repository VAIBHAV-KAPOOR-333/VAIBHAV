"""
models.py
---------
Define database tables using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from database import Base

class User(Base):
    """
    Represents the 'users' table in the database
    """
    __tablename__ = "users"

    # Primary key
    id = Column(Integer, primary_key=True)

    # Basic user information
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    address = Column(String(255), nullable=False)
    
    # Profile picture path
    dp = Column(String(255), nullable=False)

    # Account status
    is_active = Column(Boolean, default=True, nullable=False)

    # Timestamps
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
