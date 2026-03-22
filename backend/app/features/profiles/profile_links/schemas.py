"""
User Link Schemas

Pydantic schemas for user link data validation.
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid
import re


class Platform(str, Enum):
    LINKEDIN = "linkedin"
    GITHUB = "github"
    PORTFOLIO = "portfolio"
    TWITTER = "twitter"
    BEHANCE = "behance"
    DRIBBBLE = "dribbble"
    MEDIUM = "medium"
    STACKOVERFLOW = "stackoverflow"
    OTHER = "other"


class ProfileLinkBase(BaseModel):
    label: str = Field(..., min_length=1, max_length=200, description="Custom label for the link")
    url: HttpUrl = Field(..., description="Valid URL for the platform")
    platform: Platform = Field(..., description="Type of link (linkedin, github, etc)")
    is_visible: bool = Field(default=True, description="Whether the link is visible in the resume")


class ProfileLinkCreate(ProfileLinkBase):
    """Schema for creating profile link - profile_id comes from URL path"""
    pass


class ProfileLinkUpdate(BaseModel):
    label: Optional[str] = Field(None, min_length=1, max_length=200)
    url: Optional[HttpUrl] = None
    platform: Optional[Platform] = None
    is_visible: Optional[bool] = None


class ProfileLinkResponse(ProfileLinkBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
    class Config:
        from_attributes = True
