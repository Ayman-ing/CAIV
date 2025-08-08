from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Project(BaseEntity):
    __tablename__ = 'projects'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    title = Column(String)
    description = Column(String)
    start_date = Column(Date)
    end_date = Column(Date)
    project_url = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="projects")
    # embeddings relationship is inherited from BaseEntity
