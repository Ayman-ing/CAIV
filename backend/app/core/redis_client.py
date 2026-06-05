"""Redis client singleton for distributed locks and caching."""
import os
import asyncio
import logging
import redis

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None


def _get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(_get_redis_url(), decode_responses=True)
        logger.info("Redis client initialized")
    return _client


LOCK_PREFIX = "indexing:lock"
LOCK_TTL = 600


def acquire_lock(profile_uuid: str, task_id: str) -> bool:
    """Acquire a distributed lock for profile indexing. Returns True if acquired."""
    return bool(get_redis().set(f"{LOCK_PREFIX}:{profile_uuid}", task_id, nx=True, ex=LOCK_TTL))


def release_lock(profile_uuid: str) -> None:
    """Release the indexing lock."""
    get_redis().delete(f"{LOCK_PREFIX}:{profile_uuid}")


async def acquire_lock_async(profile_uuid: str, task_id: str) -> bool:
    """Async wrapper for lock acquisition (for FastAPI routes)."""
    return await asyncio.to_thread(acquire_lock, profile_uuid, task_id)


async def release_lock_async(profile_uuid: str) -> None:
    """Async wrapper for lock release (for FastAPI routes)."""
    await asyncio.to_thread(release_lock, profile_uuid)
