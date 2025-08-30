from pydantic import BaseModel, Field, validator
from datetime import datetime, date
from typing import Optional, Literal
import uuid

# Define valid degree types
DegreeType = Literal[
    "High School Diploma", "Associate", "Bachelor", "Master", "PhD", "Professional", "Certificate", "Other"
]

class EducationBase(BaseModel):
    institution: str = Field(..., min_length=1, max_length=200, description="Educational institution name")
    degree: str = Field(..., min_length=1, max_length=200, description="Degree or certification name")
    degree_type: Optional[DegreeType] = Field(None, description="Type of degree")
    field_of_study: Optional[str] = Field(None, max_length=200, description="Field of study or major")
    honors: Optional[str] = Field(None, max_length=200, description="Honors or distinctions")
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0, description="GPA (0.0 to 4.0 scale)")
    start_date: date = Field(..., description="Education start date")
    end_date: Optional[date] = Field(None, description="Education end date (None if ongoing)")
    description: Optional[str] = Field(None, max_length=1000, description="Additional description")
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class EducationCreate(EducationBase):
    """Schema for creating education - profile_id comes from URL path"""
    pass

class EducationUpdate(BaseModel):
    institution: Optional[str] = Field(None, min_length=1, max_length=200)
    degree: Optional[str] = Field(None, min_length=1, max_length=200)
    degree_type: Optional[DegreeType] = None
    field_of_study: Optional[str] = Field(None, max_length=200)
    honors: Optional[str] = Field(None, max_length=200)
    gpa: Optional[float] = Field(None, ge=0.0, le=4.0)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = Field(None, max_length=1000)
    
    @validator('end_date')
    def validate_end_date(cls, v, values):
        if v is not None and 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v

class EducationResponse(EducationBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
