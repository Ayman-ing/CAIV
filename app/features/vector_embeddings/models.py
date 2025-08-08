from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.base import Base

class VectorEmbedding(Base):
    __tablename__ = 'vector_embeddings'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    qdrant_point_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    
    # Global entity reference using the global entity_id from BaseEntity
    entity_id = Column(UUID(as_uuid=True), nullable=False)  # References BaseEntity.entity_id
    
    embedding_type = Column(String(50), nullable=False)  # 'full_text', 'summary', 'keywords'
    chunk_index = Column(Integer, default=0)  # For chunked content
    metadata_json = Column(Text)  # JSON metadata about the embedding
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        Index('idx_vector_embeddings_entity', 'entity_id'),
        Index('idx_vector_embeddings_qdrant', 'qdrant_point_id'),
    )
