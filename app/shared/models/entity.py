from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.base import Base

class BaseEntity(Base):
    """Base class for all entities that can have vector embeddings."""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    entity_id = Column(UUID(as_uuid=True), unique=True, nullable=False)  # Global entity identifier
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationship to embeddings - this will be inherited by all entities
    @declared_attr
    def embeddings(cls):
        return relationship(
            "VectorEmbedding", 
            foreign_keys="VectorEmbedding.entity_id",
            primaryjoin=f"{cls.__name__}.entity_id == VectorEmbedding.entity_id",
            cascade="all, delete-orphan"
        )
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Auto-assign entity_id if not provided
        if not self.entity_id:
            self.entity_id = uuid.uuid4()
    
    @property
    def entity_type(self):
        """Return the entity type name for this entity."""
        return self.__tablename__
