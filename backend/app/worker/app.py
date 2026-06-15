"""Celery application initialization and configuration."""
import logging
import os

from celery import Celery
from dotenv import load_dotenv

load_dotenv()

celery_app = Celery(
    'caiv',
    broker=os.getenv('REDIS_URL', 'redis://localhost:6379/0'),
    backend=os.getenv('REDIS_BACKEND_URL', 'redis://localhost:6379/1'),
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,
    task_soft_time_limit=25 * 60,
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
    result_expires=3600,
    task_default_queue='default',
    task_routes={
        'embedding.*': {'queue': 'embeddings'},
        'generation.*': {'queue': 'generation'},
    },
    task_queues={
        'default': {'exchange': 'default', 'routing_key': 'default'},
        'embeddings': {'exchange': 'embeddings', 'routing_key': 'embeddings'},
        'generation': {'exchange': 'generation', 'routing_key': 'generation'},
    },
)


def get_celery_app():
    """Return the Celery app instance."""
    return celery_app
