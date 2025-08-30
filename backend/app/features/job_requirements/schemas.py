"""
Job Requirement Schemas

Pydantic schemas for job requirement data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class RequirementCategory(str, Enum):
    EDUCATION = "Education"
    EXPERIENCE = "Experience"
    TECHNICAL_SKILLS = "Technical Skills"
    SOFT_SKILLS = "Soft Skills"
    CERTIFICATIONS = "Certifications"
    LANGUAGES = "Languages"
    OTHER = "Other"


class JobRequirementBase(BaseModel):
    requirement_text: str
    category: RequirementCategory


class JobRequirementCreate(JobRequirementBase):
    job_description_uuid: str


class JobRequirementUpdate(BaseModel):
    requirement_text: Optional[str] = None
    category: Optional[RequirementCategory] = None


class JobRequirementResponse(JobRequirementBase):
    id: int
    job_description_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
