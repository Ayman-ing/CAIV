from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

from shared.models.base import Base


class JobRequirement(Base):
    __tablename__ = 'job_requirements'
    
    id = Column(Integer, primary_key=True)
    job_description_id = Column(Integer, ForeignKey('job_descriptions.id'))
    requirement_text = Column(String)
    category = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    job_description = relationship("JobDescription", back_populates="job_requirements")