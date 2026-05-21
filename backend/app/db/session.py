"""
Database session management
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import logging

from core.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()

# Build async database URL
async_database_url = settings.DATABASE_URL
if async_database_url.startswith("postgresql://"):
    async_database_url = async_database_url.replace(
        "postgresql://", "postgresql+asyncpg://", 1
    )

engine = create_async_engine(
    async_database_url,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_db():
    """Database dependency for FastAPI"""
    async with SessionLocal() as db:
        try:
            yield db
        except SQLAlchemyError as e:
            logger.error(f"Database error: {e}")
            await db.rollback()
            raise
