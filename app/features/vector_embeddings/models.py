from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.base import Base

class Embedding(Base):
    __tablename__ = 'embeddings'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    
    # Foreign key to entity table using UUID
    entity_uuid = Column(UUID(as_uuid=True), ForeignKey('entities.uuid'), nullable=False)
    
    # Qdrant integration
    qdrant_point_id = Column(UUID(as_uuid=True), unique=True, nullable=False)
    
    # Chunking and type information
    embedding_type = Column(String(50), nullable=False)  # 'full_text', 'summary', 'keywords'
    chunk_index = Column(Integer, default=0)  # For chunked content
    
    # Rich metadata (avoid querying Qdrant for these)
    text_preview = Column(Text)  # First 200 chars for preview/debugging
    token_count = Column(Integer)  # For cost tracking
    model_name = Column(String(100))  # Which embedding model was used
    model_version = Column(String(50))  # Model version for tracking
    
    # Additional metadata as JSON
    metadata_json = Column(Text)  # Any other metadata as JSON
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    entity = relationship("Entity", back_populates="embeddings")
    
    __table_args__ = (
        Index('idx_embeddings_entity_uuid', 'entity_uuid'),
        Index('idx_embeddings_qdrant_point', 'qdrant_point_id'),
        Index('idx_embeddings_type_chunk', 'entity_uuid', 'embedding_type', 'chunk_index'),
    )
