from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from pgvector.sqlalchemy import Vector
from datetime import datetime
import uuid

from shared.models.base import Base

class Embedding(Base):
    __tablename__ = 'embeddings'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)

    entity_uuid = Column(UUID(as_uuid=True), ForeignKey('entities.uuid'), nullable=False)

    vector_data = Column(Vector(384))

    embedding_type = Column(String(50), nullable=False)
    chunk_index = Column(Integer, default=0)

    text_preview = Column(Text)
    token_count = Column(Integer)
    model_name = Column(String(100))
    model_version = Column(String(50))

    content_hash = Column(String(64), nullable=True)

    metadata_json = Column(Text)

    status = Column(String(50), default='pending')
    indexed_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    entity = relationship("Entity", back_populates="embeddings")

    __table_args__ = (
        Index('idx_embeddings_entity_uuid', 'entity_uuid'),
        Index('idx_embeddings_type_chunk', 'entity_uuid', 'embedding_type', 'chunk_index'),
    )
