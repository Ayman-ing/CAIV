from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class WorkExperience(BaseEntity):
    __tablename__ = 'work_experiences'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    job_title = Column(String)
    company = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="work_experiences")
    # embeddings relationship is inherited from BaseEntity
