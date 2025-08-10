from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class ProfileLink(BaseEntity):
    __tablename__ = 'profile_links'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # ProfileLink specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    platform = Column(String)
    url = Column(String)    # Relationships
    profile = relationship("Profile", back_populates="profile_links")
    # embeddings relationship is inherited from BaseEntity
    
    __mapper_args__ = {
        'polymorphic_identity': 'profile_link',
    }