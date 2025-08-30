from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Language(BaseEntity):
    __tablename__ = 'languages'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # Language specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    language = Column(String)
    proficiency = Column(String)  # e.g., Native, Fluent, Conversational, Basic    # Relationships
    profile = relationship("Profile", back_populates="languages")
    # embeddings relationship is inherited from BaseEntity
    
    __mapper_args__ = {
        'polymorphic_identity': 'language',
    }
