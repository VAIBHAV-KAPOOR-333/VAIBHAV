from sqlalchemy import Column, Integer, String, BigInteger
from database import Base


class Register(Base):
__tablename__ = "register"


id = Column(Integer, primary_key=True, index=True)
name = Column(String(100), nullable=False)
phone = Column(BigInteger, nullable=False)
address = Column(String(255), nullable=False)