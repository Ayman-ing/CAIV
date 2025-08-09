from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class CustomSection(BaseEntity):
    __tablename__ = 'custom_sections'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    title = Column(String)
    type = Column(String)
    content = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="custom_sections")
    # embeddings relationship is inherited from BaseEntity