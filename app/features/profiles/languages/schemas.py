from pydantic import BaseModel
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
    language: str
    proficiency: ProficiencyLevel

class LanguageCreate(LanguageBase):
    user_uuid: str

class LanguageUpdate(BaseModel):
    language: Optional[str] = None
    proficiency: Optional[ProficiencyLevel] = None

class LanguageResponse(LanguageBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
