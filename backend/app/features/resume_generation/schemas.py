from pydantic import BaseModel, Field
from typing import Optional, List
from uuid import UUID


class JDAnalysis(BaseModel):
    required_skills: List[str] = Field(default_factory=list)
    preferred_skills: List[str] = Field(default_factory=list)
    required_experience: Optional[str] = Field(None)
    key_responsibilities: List[str] = Field(default_factory=list)
    qualifications: List[str] = Field(default_factory=list)
    industry_keywords: List[str] = Field(default_factory=list)
    job_title_raw: Optional[str] = Field(None)
    company_raw: Optional[str] = Field(None)


class GenerateRequest(BaseModel):
    job_description_text: str = Field(..., min_length=50, description="The job description text to generate a resume for")


class GenerateResponse(BaseModel):
    draft_uuid: UUID = Field(..., description="UUID of the created resume draft")


class TailoredDescription(BaseModel):
    description: str


class TailoredSummary(BaseModel):
    summary: str


class TailoredDraft(BaseModel):
    """Single LLM call response tailoring all resume content at once."""
    summary: Optional[str] = Field(None, description="Tailored professional summary (only if the original had one)")
    experience_descriptions: List[str] = Field(
        description="Tailored descriptions for each work experience, in the same order as provided"
    )
    project_descriptions: List[str] = Field(
        default_factory=list,
        description="Tailored descriptions for each project, in the same order as provided"
    )
