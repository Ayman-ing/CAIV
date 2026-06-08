from sqlalchemy import Column, Integer, DateTime, String, ForeignKey, event
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from typing import TYPE_CHECKING

from shared.models.base import Base

if TYPE_CHECKING:
    from features.indexing.models import Embedding

class Entity(Base):
    """Main entity table - all domain entities inherit from this."""
    __tablename__ = 'entities'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    entity_type = Column(String(50), nullable=False)  # Discriminator for entity type
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship to embeddings - using string reference to avoid circular imports
    embeddings = relationship("Embedding", back_populates="entity", cascade="all, delete-orphan")
    
    __mapper_args__ = {
        'polymorphic_identity': 'entity',
        'polymorphic_on': entity_type,
        'with_polymorphic': '*'
    }


# Ensure updated_at gets stamped even when only child-table columns change
# (joined table inheritance only UPDATEs the parent table when a parent column
#  is in the changeset; `onupdate` alone doesn't fire in that case)
@event.listens_for(Entity, 'before_update', propagate=True)
def _touch_updated_at(mapper, connection, target):
    target.updated_at = datetime.utcnow()

class BaseEntity(Entity):
    """Base class for all specific entities that can have vector embeddings."""
    __abstract__ = True
    
    @property
    def entity_name(self):
        """Return the entity type name for this entity."""
        return self.__tablename__
