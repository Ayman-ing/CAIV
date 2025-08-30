from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class ProfessionalSummary(BaseEntity):
    __tablename__ = 'professional_summaries'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # ProfessionalSummary specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    summary_text = Column(String)    # Relationships
    profile = relationship("Profile", back_populates="professional_summaries")
    # embeddings relationship is inherited from BaseEntity
    
    __mapper_args__ = {
        'polymorphic_identity': 'professional_summarie',
    }