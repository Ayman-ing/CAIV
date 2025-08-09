from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Literal
import uuid

# Define valid skill proficiency levels
ProficiencyLevel = Literal["Beginner", "Intermediate", "Advanced", "Expert"]

class SkillBase(BaseModel):
    category: str = Field(..., min_length=1, max_length=100, description="Skill category (e.g., Programming, Design)")
    name: str = Field(..., min_length=1, max_length=200, description="Skill name")
    proficiency: Optional[ProficiencyLevel] = Field(None, description="Proficiency level")
    years_experience: Optional[int] = Field(None, ge=0, le=50, description="Years of experience with this skill")

class SkillCreate(SkillBase):
    """Schema for creating skill - profile_id comes from URL path"""
    pass

class SkillUpdate(BaseModel):
    category: Optional[str] = Field(None, min_length=1, max_length=100)
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    proficiency: Optional[ProficiencyLevel] = None
    years_experience: Optional[int] = Field(None, ge=0, le=50)

class SkillResponse(SkillBase):
    uuid: uuid.UUID
    profile_id: int = Field(..., description="Profile this skill belongs to")
    user_id: int = Field(..., description="User who owns this skill")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
