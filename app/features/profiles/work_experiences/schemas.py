from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional
import uuid

class WorkExperienceBase(BaseModel):
    job_title: str = Field(..., min_length=1, max_length=200, description="Job title")
    company: str = Field(..., min_length=1, max_length=200, description="Company name")
    start_date: date = Field(..., description="Employment start date")
    end_date: Optional[date] = Field(None, description="Employment end date (None if current)")
    description: Optional[str] = Field(None, max_length=2000, description="Job description")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class WorkExperienceCreate(WorkExperienceBase):
    """Schema for creating work experience - profile_id comes from URL path"""
    pass

class WorkExperienceUpdate(BaseModel):
    job_title: Optional[str] = Field(None, min_length=1, max_length=200)
    company: Optional[str] = Field(None, min_length=1, max_length=200)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=2000)
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    uuid: uuid.UUID
    profile_id: int = Field(..., description="Profile this work experience belongs to")
    user_id: int = Field(..., description="User who owns this work experience")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
