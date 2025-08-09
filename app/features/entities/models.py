from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from ...shared.models.base import Base

class BaseEntity(Base):
    """Base class for all entities that can have vector embeddings"""
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    @declared_attr
    def embeddings(cls):
        """Each entity can have multiple embeddings"""
        return relationship(
            "VectorEmbedding", 
            foreign_keys=f"VectorEmbedding.{cls.__name__.lower()}_id",
            back_populates=cls.__name__.lower(),
            cascade="all, delete-orphan"
        )
    
    @property
    def entity_type(self):
        """Return the entity type based on class name"""
        return self.__class__.__name__.lower()
    
    @property 
    def table_name(self):
        """Return the table name"""
        return self.__tablename__
