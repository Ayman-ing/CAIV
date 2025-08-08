"""
Vector Embedding Feature

Schema-only implementation for vector embeddings used in AI similarity matching.
"""

from .schemas import (
    VectorEmbeddingBase,
    VectorEmbeddingCreate,
    VectorEmbeddingUpdate,
    VectorEmbeddingResponse,
    EmbeddingEntityType,
)

__all__ = [
    "VectorEmbeddingBase",
    "VectorEmbeddingCreate", 
    "VectorEmbeddingUpdate",
    "VectorEmbeddingResponse",
    "EmbeddingEntityType",
]
