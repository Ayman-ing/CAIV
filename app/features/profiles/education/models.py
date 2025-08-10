from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Education(BaseEntity):
    __tablename__ = 'education'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # Education specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    institution = Column(String)
    degree = Column(String)
    field_of_study = Column(String)
    honors = Column(String)
    gpa = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    
    # Relationships
    profile = relationship("Profile", back_populates="education")
    # embeddings relationship is inherited from BaseEntity via Entity table
    
    __mapper_args__ = {
        'polymorphic_identity': 'education',
    }
