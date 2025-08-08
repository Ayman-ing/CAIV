from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Skill(BaseEntity):
    __tablename__ = 'skills'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    category = Column(String)
    name = Column(String)
    proficiency = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="skills")
    # embeddings relationship is inherited from BaseEntity
