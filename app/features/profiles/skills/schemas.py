from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid

class SkillBase(BaseModel):
    category: str
    name: str
    proficiency: Optional[str] = None

class SkillCreate(SkillBase):
    user_uuid: str

class SkillUpdate(BaseModel):
    category: Optional[str] = None
    name: Optional[str] = None
    proficiency: Optional[str] = None

class SkillResponse(SkillBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
