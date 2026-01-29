import os
import sys
from sqlalchemy import create_engine, pool
from alembic import context
from dotenv import load_dotenv

# Load env vars
load_dotenv()

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Import Base & models
from database import Base
from models import User  # ensure models are imported

# Alembic config
config = context.config

# DB URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Metadata for autogenerate
target_metadata = Base.metadata


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    engine = create_engine(
        DATABASE_URL,
        poolclass=pool.NullPool,
        echo=False,   # ✅ no SQL logs
    )

    with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
