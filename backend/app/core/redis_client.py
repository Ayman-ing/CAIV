"""Redis client singleton for distributed locks, caching, and pub/sub events."""
import os
import asyncio
import json
import logging
import redis
import redis.asyncio as redis_asyncio

logger = logging.getLogger(__name__)

_client: redis.Redis | None = None
_async_client: redis_asyncio.Redis | None = None

EVENT_CHANNEL_PREFIX = "indexing:events"


def _get_redis_url() -> str:
    return os.getenv("REDIS_URL", "redis://localhost:6379/0")


def get_redis() -> redis.Redis:
    global _client
    if _client is None:
        _client = redis.from_url(_get_redis_url(), decode_responses=True)
        logger.info("Redis client initialized")
    return _client


def get_async_redis() -> redis_asyncio.Redis:
    global _async_client
    if _async_client is None:
        _async_client = redis_asyncio.from_url(_get_redis_url(), decode_responses=True)
        logger.info("Async Redis client initialized")
    return _async_client


async def close_async_redis() -> None:
    global _async_client
    if _async_client is not None:
        await _async_client.aclose()
        _async_client = None
        logger.info("Async Redis client closed")


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


# ── Pub/Sub for indexing events ──────────────────────────────────────


def publish_event(profile_uuid: str, event_type: str, data: dict) -> None:
    """Publish an indexing event to Redis pub/sub (called from Celery tasks)."""
    channel = f"{EVENT_CHANNEL_PREFIX}:{profile_uuid}"
    payload = json.dumps({"type": event_type, "data": data})
    try:
        get_redis().publish(channel, payload)
    except Exception as e:
        logger.warning(f"Failed to publish event to {channel}: {e}")


async def subscribe_events(profile_uuid: str):
    """
    Async generator that yields SSE-formatted event strings.
    Subscribes to Redis pub/sub for a given profile's indexing events.
    Yields formatted SSE data lines. Exits on 'completed' or 'error' event.
    """
    channel = f"{EVENT_CHANNEL_PREFIX}:{profile_uuid}"
    r = get_async_redis()
    pubsub = r.pubsub()
    await pubsub.subscribe(channel)

    try:
        yield f"event: connected\ndata: {json.dumps({'type': 'connected'})}\n\n"

        async for message in pubsub.listen():
            if message["type"] != "message":
                continue

            raw = message["data"]
            parsed = json.loads(raw)
            event_type = parsed.get("type", "message")
            payload = parsed.get("data", parsed)
            yield f"event: {event_type}\ndata: {json.dumps(payload)}\n\n"

            if event_type in ("completed", "error"):
                break
    except asyncio.CancelledError:
        logger.info(f"SSE subscription cancelled for profile {profile_uuid}")
    except Exception as e:
        logger.error(f"SSE subscription error for profile {profile_uuid}: {e}")
    finally:
        await pubsub.unsubscribe(channel)
        await pubsub.close()
