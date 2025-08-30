from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum
import uuid

class ProficiencyLevel(str, Enum):
    NATIVE = "Native"
    FLUENT = "Fluent"
    CONVERSATIONAL = "Conversational"
    INTERMEDIATE = "Intermediate"
    BASIC = "Basic"

class LanguageBase(BaseModel):
    language: str = Field(..., min_length=1, max_length=100, description="Language name")
    proficiency: ProficiencyLevel = Field(..., description="Language proficiency level")
    can_read: Optional[bool] = Field(True, description="Can read in this language")
    can_write: Optional[bool] = Field(True, description="Can write in this language")
    can_speak: Optional[bool] = Field(True, description="Can speak this language")

class LanguageCreate(LanguageBase):
    """Schema for creating language - profile_id comes from URL path"""
    pass

class LanguageUpdate(BaseModel):
    language: Optional[str] = Field(None, min_length=1, max_length=100)
    proficiency: Optional[ProficiencyLevel] = None
    can_read: Optional[bool] = None
    can_write: Optional[bool] = None
    can_speak: Optional[bool] = None

class LanguageResponse(LanguageBase):
    uuid: uuid.UUID
    profile_id: int = Field(..., description="Profile this language belongs to")
    user_id: int = Field(..., description="User who owns this language")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
