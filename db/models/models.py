from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from db.session import Base
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID, JSONB

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    useruuid = Column(UUID, unique=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String)
    modules = Column(JSONB)
    two_factor = Column(Boolean, default=False)
    otp = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    

