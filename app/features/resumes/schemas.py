from pydantic import BaseModel
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

class ResumeComponentBase(BaseModel):
    component_type: ComponentType
    component_id: int
    order_index: int
    is_included: bool = True

class ResumeComponentCreate(ResumeComponentBase):
    pass

class ResumeComponentResponse(ResumeComponentBase):
    uuid: uuid.UUID
    generated_resume_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class GeneratedResumeBase(BaseModel):
    title: str
    template_name: ResumeTemplate = ResumeTemplate.MODERN
    content: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = None

class GeneratedResumeCreate(GeneratedResumeBase):
    user_uuid: str
    job_description_uuid: Optional[str] = None
    components: List[ResumeComponentCreate] = []

class GeneratedResumeUpdate(BaseModel):
    title: Optional[str] = None
    template_name: Optional[ResumeTemplate] = None
    content: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = None

class GeneratedResumeResponse(GeneratedResumeBase):
    uuid: uuid.UUID
    user_id: int
    job_description_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    components: List[ResumeComponentResponse] = []
    
    class Config:
        from_attributes = True
