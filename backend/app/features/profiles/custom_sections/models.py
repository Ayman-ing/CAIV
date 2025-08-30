from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class CustomSection(BaseEntity):
    __tablename__ = 'custom_sections'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # CustomSection specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    title = Column(String)
    type = Column(String)
    content = Column(String)    # Relationships
    profile = relationship("Profile", back_populates="custom_sections")
    # embeddings relationship is inherited from BaseEntity
    
    __mapper_args__ = {
        'polymorphic_identity': 'custom_section',
    }