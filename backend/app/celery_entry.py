"""
Celery worker entrypoint.

Run with: celery -A app.celery_entry worker -Q default,embeddings --loglevel=info

The Celery worker runs as a separate process from the FastAPI server.
It uses synchronous database sessions (psycopg2) and synchronous embedding model calls.
"""
import logging

from core.celery_app import celery_app
from core.config import get_settings
from core.logging import setup_logging

settings = get_settings()
setup_logging(settings.LOG_LEVEL, settings.effective_log_format)
logger = logging.getLogger(__name__)

logger.info("Celery worker starting — importing task modules")

import features.vector_embeddings.tasks

logger.info("All task modules loaded, worker ready")
