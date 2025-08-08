from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity
from shared.models.base import Base

class GeneratedResume(BaseEntity):
    __tablename__ = 'generated_resumes'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'),nullable=False)  # Profile-specific resumes
    job_description_id = Column(Integer, ForeignKey('job_descriptions.id'), nullable=True)
    title = Column(String)
    template_name = Column(String)  # Template used for generation
    content = Column(Text)  # Generated resume content (JSON or HTML)
    relevance_score = Column(Float, nullable=True)  # AI-calculated relevance to job
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="generated_resumes")
    
    @declared_attr
    def job_description(cls):
        return relationship("JobDescription", back_populates="generated_resumes")
    
    @declared_attr
    def resume_components(cls):
        return relationship("ResumeComponent", back_populates="generated_resume")
    # embeddings relationship is inherited from BaseEntity

class ResumeComponent(Base):
    __tablename__ = 'resume_components'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    generated_resume_id = Column(Integer, ForeignKey('generated_resumes.id'),nullable=False)
    component_type = Column(String)  # e.g., 'work_experience', 'education', 'skills'
    component_id = Column(Integer)   # ID of the actual component (work_exp, education, etc.)
    order_index = Column(Integer)    # Order in the resume
    is_included = Column(String, default=True)  # Whether to include in final resume
    created_at = Column(DateTime, default=datetime.utcnow)
    
    generated_resume = relationship("GeneratedResume", back_populates="resume_components")
