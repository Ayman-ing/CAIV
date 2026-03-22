from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
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
    proficiency = Column(String)
    can_read = Column(Boolean, default=True)
    can_write = Column(Boolean, default=True)
    can_speak = Column(Boolean, default=True)
    
    # Relationships
    profile = relationship("Profile", back_populates="languages")
    # embeddings relationship is inherited from BaseEntity
    
    # Constraints
    __table_args__ = (
        UniqueConstraint('profile_id', 'language', name='uq_profile_language'),
    )
    
    __mapper_args__ = {
        'polymorphic_identity': 'language',
    }
