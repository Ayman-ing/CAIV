from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from shared.models.entity import BaseEntity


class JobDescription(BaseEntity):
    __tablename__ = 'job_descriptions'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # JobDescription specific fields
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)    # Relationships
    user = relationship("User", back_populates="job_descriptions")
    generated_resumes = relationship("GeneratedResume", back_populates="job_description",
                                     foreign_keys="GeneratedResume.job_description_id")
    job_keywords = relationship("JobKeyword", back_populates="job_description")
    job_requirements = relationship("JobRequirement", back_populates="job_description")
    # embeddings relationship is inherited from BaseEntity
    
    __mapper_args__ = {
        'polymorphic_identity': 'job_description',
    }