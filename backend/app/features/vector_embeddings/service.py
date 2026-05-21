"""Embedding service for generating and managing vector embeddings."""
import asyncio
from typing import List, Optional
import logging
from sentence_transformers import SentenceTransformer
from core.config import get_settings

logger = logging.getLogger(__name__)

# Global embedding model instance (lazy loaded)
_embedding_model: Optional[SentenceTransformer] = None


def _get_embedding_model() -> SentenceTransformer:
    """Get or initialize the embedding model (lazy loading)."""
    global _embedding_model
    if _embedding_model is None:
        settings = get_settings()
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        _embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    return _embedding_model


class EmbeddingService:
    """Service for generating embeddings and performing vector operations."""

    @staticmethod
    async def generate_embeddings(texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts asynchronously.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors (each is a list of floats)

        Raises:
            ValueError: If texts list is empty
            RuntimeError: If embedding model fails to load
        """
        if not texts:
            raise ValueError("Cannot generate embeddings for empty text list")

        try:
            model = _get_embedding_model()

            embeddings = await asyncio.get_running_loop().run_in_executor(
                None, lambda: model.encode(texts, convert_to_tensor=False)
            )

            # Convert numpy array to list of lists
            return embeddings.tolist()

        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise RuntimeError(f"Failed to generate embeddings: {str(e)}")

    @staticmethod
    async def generate_single_embedding(text: str) -> List[float]:
        """
        Generate a single embedding for a text string.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector as list of floats

        Raises:
            ValueError: If text is empty
            RuntimeError: If embedding model fails
        """
        if not text or not text.strip():
            raise ValueError("Cannot generate embedding for empty text")

        embeddings = await EmbeddingService.generate_embeddings([text])
        return embeddings[0]

    @staticmethod
    def embedding_to_pgvector_string(embedding: List[float]) -> str:
        """
        Convert embedding list to pgvector format string.

        Deprecated: vector_data now uses native Vector(384) type.
        Kept for backward compatibility with any existing serialized data.

        Args:
            embedding: List of floats representing the embedding

        Returns:
            String representation for pgvector storage
        """
        logger.warning("embedding_to_pgvector_string is deprecated. Use native Vector type instead.")
        if not embedding:
            raise ValueError("Cannot convert empty embedding to pgvector string")
        return "[" + ",".join(str(x) for x in embedding) + "]"

    @staticmethod
    def pgvector_string_to_embedding(vector_str: str) -> List[float]:
        """
        Convert pgvector string format back to embedding list.

        Deprecated: vector_data now uses native Vector(384) type.
        Kept for backward compatibility with any existing serialized data.

        Args:
            vector_str: pgvector format string

        Returns:
            List of floats
        """
        logger.warning("pgvector_string_to_embedding is deprecated. Use native Vector type instead.")
        if not vector_str:
            raise ValueError("Cannot convert empty vector string")
        clean = vector_str.strip("[]")
        return [float(x) for x in clean.split(",")]

    @staticmethod
    def calculate_cosine_similarity(vector1: List[float], vector2: List[float]) -> float:
        """
        Calculate cosine similarity between two embedding vectors.

        Args:
            vector1: First embedding vector
            vector2: Second embedding vector

        Returns:
            Cosine similarity score (0 to 1)

        Raises:
            ValueError: If vectors have different dimensions
        """
        if len(vector1) != len(vector2):
            raise ValueError(f"Vector dimensions must match: {len(vector1)} != {len(vector2)}")

        import math

        # Calculate dot product
        dot_product = sum(a * b for a, b in zip(vector1, vector2))

        # Calculate magnitudes
        mag1 = math.sqrt(sum(a * a for a in vector1))
        mag2 = math.sqrt(sum(b * b for b in vector2))

        if mag1 == 0 or mag2 == 0:
            return 0.0

        return dot_product / (mag1 * mag2)
