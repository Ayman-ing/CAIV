"""Repository for embedding database operations."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from datetime import datetime
import logging
import uuid as python_uuid

from .models import Embedding
from core.config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingRepository:
    """Repository for managing embeddings in the database."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session."""
        self.session = session
        self.settings = get_settings()

    async def create(
        self,
        entity_uuid: str,
        vector_data: List[float],
        embedding_type: str = "full_text",
        text_preview: Optional[str] = None,
        token_count: Optional[int] = None,
        metadata_json: Optional[str] = None,
        status: str = "completed",
    ) -> Embedding:
        """
        Create a new embedding record.

        Args:
            entity_uuid: UUID of the entity being embedded
            vector_data: Embedding vector as a list of floats (384 dimensions)
            embedding_type: Type of embedding (default: full_text)
            text_preview: First 200 chars of source text
            token_count: Number of tokens in source text
            metadata_json: Additional metadata as JSON string
            status: Status of embedding (default: completed)

        Returns:
            Created Embedding instance

        Raises:
            ValueError: If entity_uuid or vector_data is invalid
        """
        if not entity_uuid or not vector_data:
            raise ValueError("entity_uuid and vector_data are required")

        try:
            embedding = Embedding(
                uuid=python_uuid.uuid4(),
                entity_uuid=python_uuid.UUID(entity_uuid),
                vector_data=vector_data,
                embedding_type=embedding_type,
                text_preview=text_preview,
                token_count=token_count,
                model_name=self.settings.EMBEDDING_MODEL,
                model_version="1.0",
                metadata_json=metadata_json,
                status=status,
                indexed_at=datetime.utcnow() if status == "completed" else None,
            )

            self.session.add(embedding)
            await self.session.flush()
            logger.info(f"Created embedding {embedding.uuid} for entity {entity_uuid}")
            return embedding

        except Exception as e:
            logger.error(f"Error creating embedding: {str(e)}")
            raise

    async def find_by_entity(
        self,
        entity_uuid: str,
        embedding_type: Optional[str] = None,
    ) -> List[Embedding]:
        """
        Find embeddings by entity UUID.

        Args:
            entity_uuid: UUID of the entity
            embedding_type: Optional filter by type

        Returns:
            List of embeddings for the entity
        """
        try:
            query = select(Embedding).where(
                Embedding.entity_uuid == python_uuid.UUID(entity_uuid)
            )

            if embedding_type:
                query = query.where(Embedding.embedding_type == embedding_type)

            result = await self.session.execute(query)
            embeddings = result.scalars().all()
            return embeddings

        except Exception as e:
            logger.error(f"Error finding embeddings for entity {entity_uuid}: {str(e)}")
            raise

    async def update_status(
        self,
        embedding_uuid: str,
        status: str,
    ) -> Optional[Embedding]:
        """
        Update the status of an embedding.

        Args:
            embedding_uuid: UUID of the embedding
            status: New status (pending, completed, failed)

        Returns:
            Updated embedding or None if not found
        """
        try:
            query = select(Embedding).where(
                Embedding.uuid == python_uuid.UUID(embedding_uuid)
            )
            result = await self.session.execute(query)
            embedding = result.scalar_one_or_none()

            if embedding:
                embedding.status = status
                if status == "completed":
                    embedding.indexed_at = datetime.utcnow()
                embedding.updated_at = datetime.utcnow()
                await self.session.flush()
                logger.info(f"Updated embedding {embedding_uuid} status to {status}")

            return embedding

        except Exception as e:
            logger.error(f"Error updating embedding status: {str(e)}")
            raise

    async def delete_by_entity(self, entity_uuid: str) -> int:
        """
        Delete all embeddings for an entity (for re-indexing).

        Args:
            entity_uuid: UUID of the entity

        Returns:
            Number of deleted embeddings
        """
        try:
            query = select(Embedding).where(
                Embedding.entity_uuid == python_uuid.UUID(entity_uuid)
            )
            result = await self.session.execute(query)
            embeddings = result.scalars().all()

            count = len(embeddings)
            for embedding in embeddings:
                await self.session.delete(embedding)

            await self.session.flush()
            logger.info(f"Deleted {count} embeddings for entity {entity_uuid}")
            return count

        except Exception as e:
            logger.error(f"Error deleting embeddings for entity: {str(e)}")
            raise

    async def find_recent(self, limit: int = 10) -> List[Embedding]:
        """
        Find recently indexed embeddings.

        Args:
            limit: Maximum number to return

        Returns:
            List of recent embeddings ordered by indexed_at descending
        """
        try:
            query = (
                select(Embedding)
                .order_by(desc(Embedding.indexed_at))
                .limit(limit)
            )
            result = await self.session.execute(query)
            return result.scalars().all()

        except Exception as e:
            logger.error(f"Error finding recent embeddings: {str(e)}")
            raise

    async def find_pending(self, limit: int = 100) -> List[Embedding]:
        """
        Find pending embeddings that haven't been completed.

        Args:
            limit: Maximum number to return

        Returns:
            List of pending embeddings
        """
        try:
            query = select(Embedding).where(
                Embedding.status == "pending"
            ).limit(limit)
            result = await self.session.execute(query)
            return result.scalars().all()

        except Exception as e:
            logger.error(f"Error finding pending embeddings: {str(e)}")
            raise
