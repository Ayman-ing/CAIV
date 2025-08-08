from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class ProfileLink(BaseEntity):
    __tablename__ = 'profile_links'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    platform = Column(String)
    url = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="profile_links")
    # embeddings relationship is inherited from BaseEntity