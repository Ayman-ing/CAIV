"""
Celery worker entrypoint.

Run with: celery -A app.worker.entry worker -Q default,embeddings,generation --loglevel=info

The module path "app.worker.entry" works when running from the backend/ directory.

The Celery worker runs as a separate process from the FastAPI server.
It uses synchronous database sessions (psycopg2) and synchronous embedding model calls.
"""
import os
import sys
import logging

# Ensure app/ directory is on sys.path so internal imports (core, features, db) resolve
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from worker.app import celery_app
from core.config import get_settings
from core.logging import setup_logging

settings = get_settings()
setup_logging(settings.LOG_LEVEL, settings.effective_log_format)
logger = logging.getLogger(__name__)

logger.info("Celery worker starting — importing task modules")

import worker.tasks.embedding
import worker.tasks.generation

logger.info("All task modules loaded, worker ready")
