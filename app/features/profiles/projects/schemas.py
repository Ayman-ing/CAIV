from pydantic import BaseModel, HttpUrl
from datetime import datetime, date
from typing import Optional
import uuid

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    start_date: date
    end_date: Optional[date] = None
    project_url: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    user_uuid: str

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    project_url: Optional[HttpUrl] = None

class ProjectResponse(ProjectBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
