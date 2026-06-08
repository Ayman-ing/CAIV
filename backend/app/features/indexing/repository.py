from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from datetime import datetime
import logging
import uuid as python_uuid

from .models import Embedding
from core.config import get_settings

logger = logging.getLogger(__name__)


class EmbeddingRepository:

    def __init__(self, session: AsyncSession):
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
        try:
            query = select(Embedding).where(
                Embedding.status == "pending"
            ).limit(limit)
            result = await self.session.execute(query)
            return result.scalars().all()

        except Exception as e:
            logger.error(f"Error finding pending embeddings: {str(e)}")
            raise
