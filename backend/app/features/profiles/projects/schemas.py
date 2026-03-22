from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime, date
from typing import Optional, List
import uuid

class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Project name")
    description: Optional[str] = Field(None, max_length=2000, description="Project description")
    start_date: date = Field(..., description="Project start date")
    end_date: Optional[date] = Field(None, description="Project end date (None if ongoing)")
    url: Optional[HttpUrl] = Field(None, description="Project URL or repository link")
    technologies: Optional[str] = Field(None, max_length=1000, description="Comma-separated technologies used")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class ProjectCreate(ProjectBase):
    """Schema for creating project - profile_id comes from URL path"""
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    url: Optional[HttpUrl] = None
    technologies: Optional[str] = Field(None, max_length=1000)
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class ProjectResponse(ProjectBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
