"""
Synchronous database session management for Celery workers.

Celery tasks run synchronously, so they use psycopg2 (sync) instead of asyncpg.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

sync_database_url = settings.DATABASE_URL
if sync_database_url.startswith("postgresql+asyncpg://"):
    sync_database_url = sync_database_url.replace(
        "postgresql+asyncpg://", "postgresql+psycopg2://", 1
    )
elif sync_database_url.startswith("postgresql://"):
    sync_database_url = sync_database_url.replace(
        "postgresql://", "postgresql+psycopg2://", 1
    )

sync_engine = create_engine(
    sync_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)

SyncSessionLocal = sessionmaker(
    bind=sync_engine,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


def get_sync_db():
    """Sync database session context manager for Celery tasks."""
    db = SyncSessionLocal()
    try:
        yield db
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Sync database error: {e}")
        raise
    finally:
        db.close()
