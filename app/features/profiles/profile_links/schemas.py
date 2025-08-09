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


class ProfileLinkBase(BaseModel):
    platform: LinkPlatform = Field(..., description="Platform type for the link")
    url: HttpUrl = Field(..., description="Valid URL for the platform")

    @validator('url')
    def validate_url_for_platform(cls, v, values):
        platform = values.get('platform')
        url_str = str(v)
        
        platform_patterns = {
            LinkPlatform.LINKEDIN: r'linkedin\.com',
            LinkPlatform.GITHUB: r'github\.com',
            LinkPlatform.TWITTER: r'(twitter\.com|x\.com)',
            LinkPlatform.BEHANCE: r'behance\.net',
            LinkPlatform.DRIBBBLE: r'dribbble\.com',
            LinkPlatform.MEDIUM: r'medium\.com',
            LinkPlatform.STACKOVERFLOW: r'stackoverflow\.com'
        }
        
        if platform in platform_patterns:
            pattern = platform_patterns[platform]
            if not re.search(pattern, url_str, re.IGNORECASE):
                raise ValueError(f'URL must be from {platform.value} domain')
        
        return v


class ProfileLinkCreate(ProfileLinkBase):
    profile_id: int = Field(..., ge=1, description="ID of the profile this link belongs to")


class ProfileLinkUpdate(BaseModel):
    platform: Optional[LinkPlatform] = None
    url: Optional[HttpUrl] = None

    @validator('url')
    def validate_url_for_platform(cls, v, values):
        if v is None:
            return v
            
        platform = values.get('platform')
        if platform is None:
            return v
            
        url_str = str(v)
        
        platform_patterns = {
            LinkPlatform.LINKEDIN: r'linkedin\.com',
            LinkPlatform.GITHUB: r'github\.com',
            LinkPlatform.TWITTER: r'(twitter\.com|x\.com)',
            LinkPlatform.BEHANCE: r'behance\.net',
            LinkPlatform.DRIBBBLE: r'dribbble\.com',
            LinkPlatform.MEDIUM: r'medium\.com',
            LinkPlatform.STACKOVERFLOW: r'stackoverflow\.com'
        }
        
        if platform in platform_patterns:
            pattern = platform_patterns[platform]
            if not re.search(pattern, url_str, re.IGNORECASE):
                raise ValueError(f'URL must be from {platform.value} domain')
        
        return v


class ProfileLinkResponse(ProfileLinkBase):
    uuid: uuid.UUID
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
