"""
User Link Schemas

Pydantic schemas for user link data validation.
"""

from pydantic import BaseModel, HttpUrl
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid


class LinkPlatform(str, Enum):
    LINKEDIN = "LinkedIn"
    GITHUB = "GitHub"
    PORTFOLIO = "Portfolio"
    TWITTER = "Twitter"
    BEHANCE = "Behance"
    DRIBBBLE = "Dribbble"
    MEDIUM = "Medium"
    STACKOVERFLOW = "StackOverflow"
    PERSONAL_WEBSITE = "Personal Website"
    OTHER = "Other"


class UserLinkBase(BaseModel):
    platform: LinkPlatform
    url: HttpUrl


class UserLinkCreate(UserLinkBase):
    pass


class UserLinkUpdate(BaseModel):
    platform: Optional[LinkPlatform] = None
    url: Optional[HttpUrl] = None


class UserLinkResponse(UserLinkBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
