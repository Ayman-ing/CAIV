"""
Outbox Event Schemas

Pydantic schemas for outbox event data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import uuid


class EventType(str, Enum):
    USER_CREATED = "user_created"
    USER_UPDATED = "user_updated"
    USER_DELETED = "user_deleted"
    RESUME_GENERATED = "resume_generated"
    RESUME_UPDATED = "resume_updated"
    RESUME_DELETED = "resume_deleted"
    JOB_MATCH_COMPLETED = "job_match_completed"
    SKILL_EXTRACTED = "skill_extracted"
    PROFILE_UPDATED = "profile_updated"


class EntityType(str, Enum):
    USER = "user"
    RESUME = "resume"
    JOB_POSTING = "job_posting"
    MATCH_RESULT = "match_result"
    PROFILE = "profile"


class OutboxEventBase(BaseModel):
    event_type: EventType
    entity_type: EntityType
    entity_id: int
    payload: Optional[Dict[str, Any]] = None


class OutboxEventCreate(OutboxEventBase):
    pass


class OutboxEventUpdate(BaseModel):
    processed: Optional[bool] = None
    error: Optional[str] = None


class OutboxEventResponse(OutboxEventBase):
    uuid: uuid.UUID
    processed: bool
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
