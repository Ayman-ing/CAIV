from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid


class ResumeDraftCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    template_name: str = Field(default='CANADIAN')
    draft_data: Dict[str, Any] = Field(default_factory=dict)


class ResumeDraftUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    template_name: Optional[str] = None
    draft_data: Optional[Dict[str, Any]] = None


class ResumeDraftResponse(BaseModel):
    uuid: uuid.UUID
    profile_id: int
    title: str
    template_name: str
    draft_data: Dict[str, Any]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
