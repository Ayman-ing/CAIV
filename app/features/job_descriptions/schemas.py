"""
Job Description Schemas

Pydantic schemas for job description data validation.
"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
import uuid


class JobDescriptionBase(BaseModel):
    url: HttpUrl


class JobDescriptionCreate(JobDescriptionBase):
    pass


class JobDescriptionUpdate(BaseModel):
    url: Optional[HttpUrl] = None


class JobDescriptionResponse(JobDescriptionBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
