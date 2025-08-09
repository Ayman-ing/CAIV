from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid

class ResumeTemplate(str, Enum):
    MODERN = "modern"
    CLASSIC = "classic"
    CREATIVE = "creative"
    MINIMAL = "minimal"
    PROFESSIONAL = "professional"

class ComponentType(str, Enum):
    WORK_EXPERIENCE = "work_experience"
    EDUCATION = "education"
    SKILLS = "skills"
    PROJECTS = "projects"
    CERTIFICATES = "certificates"
    LANGUAGES = "languages"
    CUSTOM_SECTIONS = "custom_sections"

class ResumeComponentBase(BaseModel):
    component_type: ComponentType = Field(..., description="Type of component to include")
    component_id: int = Field(..., ge=1, description="ID of the specific component")
    order_index: int = Field(..., ge=0, le=100, description="Display order of this component")
    is_included: bool = Field(True, description="Whether to include this component")

class ResumeComponentCreate(ResumeComponentBase):
    pass

class ResumeComponentUpdate(BaseModel):
    component_type: Optional[ComponentType] = None
    component_id: Optional[int] = Field(None, ge=1)
    order_index: Optional[int] = Field(None, ge=0, le=100)
    is_included: Optional[bool] = None

class ResumeComponentResponse(ResumeComponentBase):
    uuid: uuid.UUID
    generated_resume_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GeneratedResumeBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title for the generated resume")
    template_name: ResumeTemplate = Field(ResumeTemplate.MODERN, description="Template to use for the resume")
    content: Optional[Dict[str, Any]] = Field(None, description="Generated content in structured format")
    relevance_score: Optional[float] = Field(None, ge=0.0, le=100.0, description="AI-generated relevance score")

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('relevance_score')
    def validate_relevance_score(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Relevance score must be between 0 and 100')
        return v

class GeneratedResumeCreate(GeneratedResumeBase):
    profile_id: int = Field(..., ge=1, description="ID of the profile to generate resume for")
    job_description_id: Optional[int] = Field(None, ge=1, description="ID of job description to optimize for")
    components: List[ResumeComponentCreate] = Field(default=[], description="Components to include in the resume")

class GeneratedResumeUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    template_name: Optional[ResumeTemplate] = None
    content: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = Field(None, ge=0.0, le=100.0)

    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('relevance_score')
    def validate_relevance_score(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError('Relevance score must be between 0 and 100')
        return v

class GeneratedResumeResponse(GeneratedResumeBase):
    uuid: uuid.UUID
    profile_id: int
    job_description_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    components: List[ResumeComponentResponse] = Field(default=[], description="Components included in the resume")
    
    class Config:
        from_attributes = True
