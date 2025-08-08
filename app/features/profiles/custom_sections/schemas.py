"""
Custom Section Schemas

Pydantic schemas for custom section data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class CustomSectionBase(BaseModel):
    title: str
    content: str
    order_index: Optional[int] = 0


class CustomSectionCreate(CustomSectionBase):
    pass


class CustomSectionUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order_index: Optional[int] = None


class CustomSectionResponse(CustomSectionBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
