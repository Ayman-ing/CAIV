from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
import uuid

class EducationBase(BaseModel):
    institution: str
    degree: str
    field_of_study: Optional[str] = None
    honors: Optional[str] = None
    gpa: Optional[float] = None
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class EducationCreate(EducationBase):
    user_uuid: str

class EducationUpdate(BaseModel):
    institution: Optional[str] = None
    degree: Optional[str] = None
    field_of_study: Optional[str] = None
    honors: Optional[str] = None
    gpa: Optional[float] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class EducationResponse(EducationBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
