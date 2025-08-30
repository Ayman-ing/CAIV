"""
Vector Embedding Schemas

Pydantic schemas for vector embedding data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any
from enum import Enum
import uuid


class EmbeddingEntityType(str, Enum):
    USER_PROFILE = "user_profile"
    WORK_EXPERIENCE = "work_experience"
    PROJECT = "project"
    SKILL = "skill"
    EDUCATION = "education"
    CERTIFICATE = "certificate"
    LANGUAGE = "language"
    RESUME = "resume"
    JOB_POSTING = "job_posting"
    JOB_DESCRIPTION = "job_description"


class VectorEmbeddingBase(BaseModel):
    entity_type: EmbeddingEntityType
    entity_id: int
    qdrant_point_id: uuid.UUID
    chunk_index: Optional[int] = 0
    metadata: Optional[Dict[str, Any]] = None


class VectorEmbeddingCreate(VectorEmbeddingBase):
    pass


class VectorEmbeddingUpdate(BaseModel):
    qdrant_point_id: Optional[uuid.UUID] = None
    chunk_index: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None


class VectorEmbeddingResponse(VectorEmbeddingBase):
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
