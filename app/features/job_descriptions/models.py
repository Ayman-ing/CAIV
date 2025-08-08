from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid
from shared.models.entity import BaseEntity


class JobDescription(BaseEntity):
    __tablename__ = 'job_descriptions'
    
    user_id = Column(Integer, ForeignKey('users.id'))
    url = Column(String)
    
    @declared_attr
    def user(cls):
        return relationship("User", back_populates="job_descriptions")
    
    @declared_attr
    def generated_resumes(cls):
        return relationship("GeneratedResume", back_populates="job_description")
    
    @declared_attr
    def job_keywords(cls):
        return relationship("JobKeyword", back_populates="job_description")
    
    @declared_attr
    def job_requirements(cls):
        return relationship("JobRequirement", back_populates="job_description")
    # embeddings relationship is inherited from BaseEntity