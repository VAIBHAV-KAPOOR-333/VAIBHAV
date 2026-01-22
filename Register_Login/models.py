"""
models.py
---------
Define your database tables using SQLAlchemy ORM.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from database import Base

class User(Base):
    """
    Represents a user in the database.
    """
    __tablename__ = "users"  # Table name in the database

    # -----------------------------
    # PRIMARY KEY
    # -----------------------------
    id = Column(Integer, primary_key=True)

    # -----------------------------
    # BASIC USER INFO
    # -----------------------------
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    address = Column(String(255), nullable=False)

    # -----------------------------
    # PROFILE PICTURE PATH
    # -----------------------------
    dp = Column(String(255), nullable=False)

    # -----------------------------
    # ACCOUNT STATUS
    # -----------------------------
    is_active = Column(Boolean, default=True, nullable=False)

    # -----------------------------
    # TIMESTAMPS
    # -----------------------------
    # automatically set on insert
    created_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    # automatically updated on update
    updated_at = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"), nullable=False)

# -----------------------------
# NOTES FOR BEGINNERS
# -----------------------------
# - Column(): defines a field in the table
# - primary_key=True: marks the column as the table's primary key
# - unique=True: ensures values are unique
# - nullable=False: value is required
# - server_default=text(...): default value set by DB server
# - Alembic will read this model to generate migrations
