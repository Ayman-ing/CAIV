from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class WorkExperience(BaseEntity):
    __tablename__ = 'work_experiences'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # WorkExperience specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    job_title = Column(String)
    company = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    
    # Relationships
    profile = relationship("Profile", back_populates="work_experiences")
    # embeddings relationship is inherited from BaseEntity via Entity table
    
    __mapper_args__ = {
        'polymorphic_identity': 'work_experience',
    }
