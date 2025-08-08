from sqlalchemy import Column, Integer, String, Date, Float, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Education(BaseEntity):
    __tablename__ = 'education'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    institution = Column(String)
    degree = Column(String)
    field_of_study = Column(String)
    honors = Column(String)
    gpa = Column(Float)
    start_date = Column(Date)
    end_date = Column(Date)
    description = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="education")
    # embeddings relationship is inherited from BaseEntity
