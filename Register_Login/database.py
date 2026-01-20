"""
database.py
------------
This file handles database connection and session creation using SQLAlchemy.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load variables from .env
load_dotenv()

# Read the DATABASE_URL environment variable
DATABASE_URL = os.getenv("DATABASE_URL") or ""

print("[DB] Connecting to database:", DATABASE_URL)

# Create SQLAlchemy engine
# echo=True prints all SQL queries for debugging
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

# Create a session factory
SessionLocal = sessionmaker(bind=engine)

# Base class for ORM models
Base = declarative_base()
