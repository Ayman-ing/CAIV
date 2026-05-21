"""Celery application initialization and configuration."""
import logging
import os

from celery import Celery
from celery.schedules import crontab
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def _init_worker_logging():
    """Configure logging for Celery worker processes.
    
    Called once per worker process via the worker_process_init signal.
    """
    from core.config import get_settings
    from core.logging import setup_logging

    settings = get_settings()
    setup_logging(settings.LOG_LEVEL, settings.effective_log_format)
    logging.getLogger(__name__).info(
        "Celery worker logging initialized (level=%s, format=%s)",
        settings.LOG_LEVEL,
        settings.effective_log_format,
    )


from celery.signals import worker_process_init


@worker_process_init.connect(weak=False)
def on_worker_process_init(**kwargs):
    _init_worker_logging()


# Create Celery app
celery_app = Celery(
    'caiv',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/1'),
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    # Task configuration
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes hard limit
    task_soft_time_limit=25 * 60,  # 25 minutes soft limit
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    # Result backend configuration
    result_expires=3600,  # Results expire after 1 hour
    # Task routing
    task_default_queue='default',
    task_routes={
        'embedding.*': {'queue': 'embeddings'},
    },
    task_queues={
        'default': {'exchange': 'default', 'routing_key': 'default'},
        'embeddings': {'exchange': 'embeddings', 'routing_key': 'embeddings'},
    },
)


def get_celery_app():
    """Return the Celery app instance."""
    return celery_app
