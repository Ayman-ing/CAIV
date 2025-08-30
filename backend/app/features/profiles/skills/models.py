from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Skill(BaseEntity):
    __tablename__ = 'skills'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # Skill specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    category = Column(String)
    name = Column(String)
    proficiency = Column(String)
    
    # Relationships
    profile = relationship("Profile", back_populates="skills")
    # embeddings relationship is inherited from BaseEntity via Entity table
    
    __mapper_args__ = {
        'polymorphic_identity': 'skill',
    }
