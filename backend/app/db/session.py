"""
Database session management
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Create synchronous engine and session factory
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine,expire_on_commit=False)

# Create async engine and session factory for background tasks
async_database_url = settings.DATABASE_URL
if async_database_url.startswith("postgresql://"):
    async_database_url = async_database_url.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )

async_engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

def get_db():
    """Database dependency for FastAPI"""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.error(f"Database error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def get_async_session():
    """Async database session factory for background tasks."""
    return AsyncSessionLocal
