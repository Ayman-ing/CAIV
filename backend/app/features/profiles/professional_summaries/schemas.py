"""
Professional Summary Schemas

Pydantic schemas for professional summary data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class ProfessionalSummaryBase(BaseModel):
    title: str
    content: str


class ProfessionalSummaryCreate(ProfessionalSummaryBase):
    pass


class ProfessionalSummaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_default: Optional[bool] = None


class ProfessionalSummaryResponse(ProfessionalSummaryBase):
    uuid: uuid.UUID
    is_default: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
