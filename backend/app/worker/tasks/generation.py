import logging
from typing import List

from worker.app import celery_app
from features.indexing.service import EmbeddingService

logger = logging.getLogger(__name__)


@celery_app.task(
    name="generation.embed_text",
    queue="generation",
    bind=True,
    max_retries=3,
    acks_late=True,
)
def embed_text_task(self, text: str) -> List[float]:
    if not text or not text.strip():
        raise ValueError("Cannot embed empty text")
    logger.info("Generating embedding for text (%d chars)", len(text))
    return EmbeddingService.generate_single_embedding_sync(text)
