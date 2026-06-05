"""
Vector Embedding Schemas

Pydantic schemas for vector embedding data validation.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List
import uuid


class EmbeddingCreate(BaseModel):
    entity_uuid: str
    vector_data: List[float]
    embedding_type: str = "full_text"
    text_preview: Optional[str] = None
    token_count: Optional[int] = None
    metadata_json: Optional[str] = None


class EmbeddingUpdate(BaseModel):
    status: Optional[str] = None
    vector_data: Optional[List[float]] = None
    text_preview: Optional[str] = None
    token_count: Optional[int] = None


class EmbeddingResponse(BaseModel):
    uuid: uuid.UUID
    entity_uuid: uuid.UUID
    embedding_type: str
    text_preview: Optional[str] = None
    token_count: Optional[int] = None
    model_name: Optional[str] = None
    status: str
    indexed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class IndexingTaskResponse(BaseModel):
    task_id: str
    status: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
