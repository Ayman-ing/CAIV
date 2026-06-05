"""Embedding service for generating and managing vector embeddings."""
import asyncio
import math
from typing import List, Optional
import logging
from sentence_transformers import SentenceTransformer
from core.config import get_settings

logger = logging.getLogger(__name__)

_embedding_model: Optional[SentenceTransformer] = None


def _get_embedding_model() -> SentenceTransformer:
    """Get or initialize the embedding model (lazy loaded, shared by sync and async paths)."""
    global _embedding_model
    if _embedding_model is None:
        settings = get_settings()
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        try:
            _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL, device='cpu')
        except Exception as e:
            logger.error(f"Failed to load embedding model: {e}")
            raise RuntimeError(f"Failed to load embedding model {settings.EMBEDDING_MODEL}: {e}")
    return _embedding_model


class EmbeddingService:

    @staticmethod
    def generate_embeddings_sync(
        texts: List[str],
        batch_size: int = 10,
    ) -> List[List[float]]:
        """
        Generate embeddings synchronously (for Celery workers).

        Args:
            texts: List of text strings to embed
            batch_size: Number of texts per batch

        Returns:
            List of embedding vectors
        """
        if not texts:
            raise ValueError("Cannot generate embeddings for empty text list")

        model = _get_embedding_model()
        all_embeddings: List[List[float]] = []

        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            logger.debug(f"Encoding batch {i // batch_size + 1}/{(len(texts) - 1) // batch_size + 1} ({len(batch)} texts)")
            batch_embeddings = model.encode(batch, convert_to_tensor=False)
            all_embeddings.extend(batch_embeddings.tolist())

        return all_embeddings

    @staticmethod
    def generate_single_embedding_sync(text: str) -> List[float]:
        """Generate a single embedding synchronously."""
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")
        return EmbeddingService.generate_embeddings_sync([text])[0]

    @staticmethod
    async def generate_embeddings(texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings asynchronously (for FastAPI request path).

        Offloads the sync model.encode() to a thread pool to avoid blocking the event loop.
        """
        if not texts:
            raise ValueError("Cannot generate embeddings for empty text list")

        try:
            model = _get_embedding_model()
            embeddings = await asyncio.get_running_loop().run_in_executor(
                None, lambda: model.encode(texts, convert_to_tensor=False)
            )
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")

    @staticmethod
    async def generate_single_embedding(text: str) -> List[float]:
        """Generate a single embedding asynchronously."""
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")
        embeddings = await EmbeddingService.generate_embeddings([text])
        return embeddings[0]

    @staticmethod
    def calculate_cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
        """Calculate cosine similarity between two embedding vectors."""
        if len(vector1) != len(vector2):
            raise ValueError(f"Vector dimensions must match: {len(vector1)} != {len(vector2)}")

        import math

        dot_product = sum(a * b for a, b in zip(vector1, vector2))
        mag1 = math.sqrt(sum(a * a for a in vector1))
        mag2 = math.sqrt(sum(b * b for b in vector2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)
