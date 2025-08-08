"""
Profile Schemas

Pydantic schemas for profile data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
import uuid


class ProfileBase(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    specializations: Optional[List[str]] = None
    career_objectives: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    specializations: Optional[List[str]] = None
    career_objectives: Optional[str] = None


class ProfileResponse(ProfileBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
