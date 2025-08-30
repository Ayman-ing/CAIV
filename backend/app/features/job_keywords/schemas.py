"""
Job Keyword Schemas

Pydantic schemas for job keyword data validation.
"""

from pydantic import BaseModel
from typing import Optional
import uuid


class JobKeywordBase(BaseModel):
    keyword: str


class JobKeywordCreate(JobKeywordBase):
    job_description_uuid: str


class JobKeywordUpdate(BaseModel):
    keyword: Optional[str] = None


class JobKeywordResponse(JobKeywordBase):
    id: int
    job_description_id: int
    
    class Config:
        from_attributes = True
