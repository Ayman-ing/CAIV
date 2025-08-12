from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.base import Base

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False,index=True)
    first_name = Column(String, nullable=False)  # Now required
    last_name = Column(String, nullable=False)   # Now required
    location = Column(String)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    profiles = relationship("Profile", back_populates="user")
    job_descriptions = relationship("JobDescription", back_populates="user")