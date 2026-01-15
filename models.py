from sqlalchemy import Column, Integer, String, Boolean, DateTime, text
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)

    phone = Column(Integer, nullable=False, unique=True)
    address = Column(String(255), nullable=False)  # 👈 compulsory
    dp = Column(String(255), nullable=False)       # 👈 compulsory

    is_active = Column(Boolean, nullable=False, server_default=text("1"))

    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )

    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )
