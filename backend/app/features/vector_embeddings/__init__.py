"""
Vector Embedding Feature

Embedding generation, storage (pgvector), and indexing for AI similarity matching.
"""

from .schemas import (
    EmbeddingCreate,
    EmbeddingUpdate,
    EmbeddingResponse,
    IndexingTaskResponse,
)

__all__ = [
    "EmbeddingCreate",
    "EmbeddingUpdate",
    "EmbeddingResponse",
    "IndexingTaskResponse",
]
