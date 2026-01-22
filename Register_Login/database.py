"""
database.py
-----------
Handles database connection and sessions using SQLAlchemy.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Load environment variables from .env
load_dotenv()

# DATABASE_URL is read from .env
# Example format: mysql+pymysql://username:password@host:port/db_name
DATABASE_URL = os.getenv("DATABASE_URL")

# -----------------------------
# CREATE SQLALCHEMY ENGINE
# -----------------------------
# Engine is the core interface to the database
# echo=True prints all SQL queries (useful for debugging)
engine = create_engine(DATABASE_URL, pool_pre_ping=True, echo=True)

# -----------------------------
# CREATE DATABASE SESSION FACTORY
# -----------------------------
# SessionLocal is a factory for database sessions
SessionLocal = sessionmaker(bind=engine)

# -----------------------------
# BASE CLASS FOR MODELS
# -----------------------------
# All models should inherit from this Base
Base = declarative_base()

# -----------------------------
# NOTE ON ALEMBIC
# -----------------------------
# Alembic is a tool to manage database migrations.
# Recommended workflow:
# 1. Define your models (classes inheriting from Base)
# 2. Run `alembic revision --autogenerate -m "initial"`
# 3. Run `alembic upgrade head` to create tables
# Avoid calling Base.metadata.create_all() in production if using Alembic.
