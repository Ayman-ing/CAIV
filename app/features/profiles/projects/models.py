from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Project(BaseEntity):
    __tablename__ = 'projects'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # Project specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    title = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    project_url = Column(String)
    
    # Relationships
    profile = relationship("Profile", back_populates="projects")
    # embeddings relationship is inherited from BaseEntity via Entity table
    
    __mapper_args__ = {
        'polymorphic_identity': 'project',
    }
