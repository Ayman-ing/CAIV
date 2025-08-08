from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional
import uuid

class WorkExperienceBase(BaseModel):
    job_title: str
    company: str
    start_date: date
    end_date: Optional[date] = None
    description: Optional[str] = None

class WorkExperienceCreate(WorkExperienceBase):
    user_uuid: str  # Use UUID instead of user_id

class WorkExperienceUpdate(BaseModel):
    job_title: Optional[str] = None
    company: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None

class WorkExperienceResponse(WorkExperienceBase):
    id: int
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
