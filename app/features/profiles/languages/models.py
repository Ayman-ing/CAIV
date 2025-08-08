from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Language(BaseEntity):
    __tablename__ = 'languages'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    language = Column(String)
    proficiency = Column(String)  # e.g., Native, Fluent, Conversational, Basic
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="languages")
    # embeddings relationship is inherited from BaseEntity
