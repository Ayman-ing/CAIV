"""
Custom Section Schemas

Pydantic schemas for custom section data validation.
"""

from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional
import uuid


class CustomSectionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Title of the custom section")
    content: str = Field(..., min_length=1, max_length=10000, description="Content of the custom section")
    order_index: Optional[int] = Field(0, ge=0, le=100, description="Display order of this section")

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip()

    @validator('content')
    def validate_content(cls, v):
        if not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')
        return v.strip()


class CustomSectionCreate(CustomSectionBase):
    profile_id: int = Field(..., ge=1, description="ID of the profile this section belongs to")


class CustomSectionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    content: Optional[str] = Field(None, min_length=1, max_length=10000)
    order_index: Optional[int] = Field(None, ge=0, le=100)

    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Title cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('content')
    def validate_content(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Content cannot be empty or whitespace only')
        return v.strip() if v else v


class CustomSectionResponse(CustomSectionBase):
    uuid: uuid.UUID
    profile_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
