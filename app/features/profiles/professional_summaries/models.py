from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class ProfessionalSummary(BaseEntity):
    __tablename__ = 'professional_summaries'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    summary_text = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="professional_summaries")
    # embeddings relationship is inherited from BaseEntity