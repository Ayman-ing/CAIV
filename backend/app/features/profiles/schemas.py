"""
Profile Schemas

Pydantic schemas for profile data validation.
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid


class ProfileBase(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None  # Professional/public email (can be different from login email)
    phone_number: Optional[str] = None  # Moved from User model
    location: Optional[str] = None      # Moved from User model


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None    # Professional/public email (different from login email)
    phone_number: Optional[str] = None  # Moved from User model
    location: Optional[str] = None      # Moved from User model


class ProfileResponse(ProfileBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
