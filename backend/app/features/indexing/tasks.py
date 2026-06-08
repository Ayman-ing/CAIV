import hashlib
import logging
from datetime import datetime
import uuid
from typing import List, Optional

from sqlalchemy import select

from core.celery_app import celery_app
from core.config import get_settings
from core.redis_client import release_lock, publish_event
from db.sync_session import SyncSessionLocal
from .service import EmbeddingService
from .text_formatter import TextFormatter
from .models import Embedding

logger = logging.getLogger(__name__)

settings = get_settings()


def _content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _get_existing_hashes(session, profile_uuid: str) -> dict[str, str]:
    from features.profiles.models import Profile

    profile = session.execute(
        select(Profile).where(Profile.uuid == profile_uuid)
    ).scalars().first()
    if not profile:
        return {}

    profile_id = profile.id

    entity_uuids: list[str] = []
    for model_class, _, _ in TextFormatter.get_sections_config():
        items = session.execute(
            select(model_class.uuid).where(model_class.profile_id == profile_id)
        ).scalars().all()
        entity_uuids.extend(str(u) for u in items)

    if not entity_uuids:
        return {}

    uuids = [uuid.UUID(eid) for eid in entity_uuids]
    rows = session.execute(
        select(Embedding.entity_uuid, Embedding.content_hash).where(
            Embedding.entity_uuid.in_(uuids),
            Embedding.content_hash.isnot(None),
        )
    ).all()

    return {str(row.entity_uuid): row.content_hash for row in rows}


def _delete_embeddings_for_entity(session, entity_uuid: str) -> int:
    result = session.execute(
        select(Embedding).where(Embedding.entity_uuid == uuid.UUID(entity_uuid))
    )
    embeddings = result.scalars().all()
    count = len(embeddings)
    for emb in embeddings:
        session.delete(emb)
    if count:
        logger.debug(f"Deleted {count} embedding(s) for entity {entity_uuid}")
    return count


def _create_embedding(
    session,
    entity_uuid: str,
    vector_data: List[float],
    content_hash: str,
    embedding_type: str = "full_text",
    text_preview: str | None = None,
    token_count: int | None = None,
    status: str = "completed",
) -> Embedding:
    embedding = Embedding(
        uuid=uuid.uuid4(),
        entity_uuid=uuid.UUID(entity_uuid),
        vector_data=vector_data,
        embedding_type=embedding_type,
        content_hash=content_hash,
        text_preview=text_preview,
        token_count=token_count,
        model_name=settings.EMBEDDING_MODEL,
        model_version="1.0",
        status=status,
        indexed_at=datetime.utcnow() if status == "completed" else None,
    )
    session.add(embedding)
    session.flush()
    logger.debug(f"Created embedding {embedding.uuid} for entity {entity_uuid}")
    return embedding


@celery_app.task(
    name="embedding.index_profile",
    bind=True,
    max_retries=3,
    time_limit=600,
    soft_time_limit=550,
)
def index_profile_task(self, profile_uuid: str) -> dict:
    import time
    overall_start = time.monotonic()

    stats = {
        "profile_uuid": str(profile_uuid),
        "started_at": datetime.utcnow().isoformat(),
        "total_items": 0,
        "skipped": 0,
        "successful": 0,
        "failed": 0,
        "errors": [],
        "sections": {},
    }

    session = SyncSessionLocal()
    try:
        from features.profiles.models import Profile

        profile = session.execute(
            select(Profile).where(Profile.uuid == profile_uuid)
        ).scalars().first()
        if not profile:
            raise ValueError(f"Profile not found: {profile_uuid}")

        profile_id = profile.id
        sections_config = TextFormatter.get_sections_config()

        existing_hashes = _get_existing_hashes(session, profile_uuid)

        entity_items: List[tuple[str, str, str, str]] = []
        section_stats: dict = {}

        for model, text_fn, section_name in sections_config:
            items = session.execute(
                select(model).where(model.profile_id == profile_id)
            ).scalars().all()

            if not items:
                section_stats[section_name] = {"count": 0, "duration_s": 0}
                continue

            for item in items:
                text = text_fn(item)
                if not text or not text.strip():
                    continue
                e_uuid = str(item.uuid)
                h = _content_hash(text)
                entity_items.append((e_uuid, text, section_name, h))

        stats["total_items"] = len(entity_items)

        publish_event(profile_uuid, "progress", {
            "current": 0,
            "total": len(entity_items),
            "phase": "collecting",
            "skipped": 0,
        })

        if not entity_items:
            logger.info(f"No items to index for profile {profile_uuid}")
            stats["duration_s"] = round(time.monotonic() - overall_start, 2)
            stats["completed_at"] = datetime.utcnow().isoformat()
            session.commit()
            publish_event(profile_uuid, "completed", {"stats": stats, "message": "No items to index"})
            return stats

        unchanged: List[tuple[str, str, str, str]] = []
        changed: List[tuple[str, str, str, str]] = []

        for item in entity_items:
            e_uuid, text, section_name, h = item
            existing_hash = existing_hashes.get(e_uuid)
            if existing_hash == h:
                unchanged.append(item)
            else:
                changed.append(item)

        stats["skipped"] = len(unchanged)
        logger.info(
            f"Change detection: {len(changed)} changed, {len(unchanged)} unchanged "
            f"out of {len(entity_items)} total"
        )

        publish_event(profile_uuid, "progress", {
            "current": 0,
            "total": len(changed),
            "phase": "analyzing",
            "skipped": len(unchanged),
        })

        if not changed:
            logger.info(f"Nothing changed for profile {profile_uuid}, skipping entirely")
            stats["successful"] = stats["skipped"]
            stats["duration_s"] = round(time.monotonic() - overall_start, 2)
            stats["completed_at"] = datetime.utcnow().isoformat()
            session.commit()
            publish_event(profile_uuid, "completed", {"stats": stats, "message": "Nothing changed"})
            return stats

        batch_size = settings.EMBEDDING_BATCH_SIZE
        total_changed = len(changed)

        self.update_state(
            state="PROGRESS",
            meta={"current": 0, "total": total_changed, "phase": "embedding", "skipped": len(unchanged)},
        )
        publish_event(profile_uuid, "progress", {
            "current": 0,
            "total": total_changed,
            "phase": "embedding",
            "skipped": len(unchanged),
        })

        embedding_vectors = []
        try:
            for batch_start in range(0, total_changed, batch_size):
                batch_end = min(batch_start + batch_size, total_changed)
                batch = changed[batch_start:batch_end]
                batch_texts = [item[1] for item in batch]

                batch_vectors = EmbeddingService.generate_embeddings_sync(
                    batch_texts, batch_size=len(batch_texts)
                )
                embedding_vectors.extend(batch_vectors)

                publish_event(profile_uuid, "progress", {
                    "current": batch_end,
                    "total": total_changed,
                    "phase": "embedding",
                    "skipped": len(unchanged),
                })
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            stats["errors"].append(f"Embedding generation failed: {str(e)}")
            stats["failed"] = total_changed
            stats["duration_s"] = round(time.monotonic() - overall_start, 2)
            stats["completed_at"] = datetime.utcnow().isoformat()
            session.commit()
            return stats

        for i, (e_uuid, text, section_name, h) in enumerate(changed):
            try:
                _delete_embeddings_for_entity(session, e_uuid)

                embedding_vector = embedding_vectors[i]
                text_preview = TextFormatter.extract_text_preview(text)
                token_count = max(1, len(text) // 4)

                _create_embedding(
                    session,
                    entity_uuid=e_uuid,
                    vector_data=embedding_vector,
                    content_hash=h,
                    text_preview=text_preview,
                    token_count=token_count,
                )
                stats["successful"] += 1

                publish_event(profile_uuid, "entity_indexed", {
                    "entity_uuid": e_uuid,
                    "section": section_name,
                    "status": "completed",
                })

                if (i + 1) % 5 == 0 or i == len(changed) - 1:
                    self.update_state(
                        state="PROGRESS",
                        meta={
                            "current": i + 1,
                            "total": len(changed),
                            "phase": "persisting",
                            "skipped": len(unchanged),
                            "section": section_name,
                        },
                    )
                    publish_event(profile_uuid, "progress", {
                        "current": i + 1,
                        "total": len(changed),
                        "phase": "persisting",
                        "skipped": len(unchanged),
                        "section": section_name,
                    })

                prev = section_stats.get(section_name, {"count": 0, "duration_s": 0})
                prev["count"] = prev.get("count", 0) + 1
                section_stats[section_name] = prev

            except Exception as e:
                logger.error(f"Failed to create embedding for {e_uuid}: {e}")
                stats["failed"] += 1
                stats["errors"].append(f"{section_name}/{e_uuid}: {str(e)}")
                publish_event(profile_uuid, "entity_indexed", {
                    "entity_uuid": e_uuid,
                    "section": section_name,
                    "status": "failed",
                    "error": str(e),
                })

        for section_name in section_stats:
            section_stats[section_name]["duration_s"] = round(
                time.monotonic() - overall_start, 2
            )

        stats["sections"] = section_stats
        session.commit()

        overall_dur = time.monotonic() - overall_start
        stats["duration_s"] = round(overall_dur, 2)
        stats["completed_at"] = datetime.utcnow().isoformat()

        publish_event(profile_uuid, "completed", {"stats": stats})

        logger.info(
            f"Indexing finished for profile {profile_uuid}: "
            f"{stats['successful']} updated, {stats['skipped']} skipped, "
            f"{stats['failed']} failed in {overall_dur:.2f}s"
        )
        return stats

    except Exception as e:
        overall_dur = time.monotonic() - overall_start
        logger.error(f"Error during profile indexing: {e}")
        session.rollback()
        stats["errors"].append(str(e))
        stats["failed"] = stats.get("failed", 0) + max(
            stats["total_items"] - stats["successful"] - stats["skipped"], 1
        )
        stats["duration_s"] = round(overall_dur, 2)
        stats["completed_at"] = datetime.utcnow().isoformat()
        publish_event(profile_uuid, "error", {"message": str(e), "stats": stats})
        return stats

    finally:
        session.close()
        release_lock(profile_uuid)
        logger.info(f"Released indexing lock for profile {profile_uuid}")


@celery_app.task(
    name="embedding.index_entity",
    bind=True,
    max_retries=2,
)
def index_entity_task(self, entity_uuid: str, entity_type: str, text: str,
                      profile_uuid: Optional[str] = None) -> dict:
    result = {
        "entity_uuid": str(entity_uuid),
        "entity_type": entity_type,
        "status": "failed",
        "embedding_uuid": None,
        "error": None,
    }

    if not text or not text.strip():
        result["error"] = "Empty text provided"
        logger.warning(f"Empty text for entity {entity_uuid}")
        if profile_uuid:
            publish_event(profile_uuid, "entity_indexed", {
                "entity_uuid": entity_uuid,
                "section": entity_type,
                "status": "failed",
                "error": "Empty text",
            })
        release_lock(f"entity:{entity_uuid}")
        return result

    session = SyncSessionLocal()
    try:
        h = _content_hash(text)
        existing = session.execute(
            select(Embedding).where(
                Embedding.entity_uuid == uuid.UUID(entity_uuid),
                Embedding.content_hash == h,
            )
        ).scalars().first()

        if existing:
            logger.info(f"Entity {entity_uuid} unchanged, skipping")
            result["status"] = "completed"
            result["embedding_uuid"] = str(existing.uuid)
            result["skipped"] = True
            if profile_uuid:
                publish_event(profile_uuid, "entity_indexed", {
                    "entity_uuid": entity_uuid,
                    "section": entity_type,
                    "status": "skipped",
                })
            return result

        _delete_embeddings_for_entity(session, entity_uuid)

        embedding_vector = EmbeddingService.generate_single_embedding_sync(text)
        text_preview = TextFormatter.extract_text_preview(text)
        token_count = max(1, len(text) // 4)

        embedding = _create_embedding(
            session,
            entity_uuid=entity_uuid,
            vector_data=embedding_vector,
            content_hash=h,
            text_preview=text_preview,
            token_count=token_count,
        )

        session.commit()
        result["status"] = "completed"
        result["embedding_uuid"] = str(embedding.uuid)
        logger.info(f"Created embedding {embedding.uuid} for entity {entity_uuid} ({entity_type})")

        if profile_uuid:
            publish_event(profile_uuid, "entity_indexed", {
                "entity_uuid": entity_uuid,
                "section": entity_type,
                "status": "completed",
            })
            publish_event(profile_uuid, "completed", {"message": f"Entity {entity_uuid} indexed"})

    except Exception as e:
        session.rollback()
        result["error"] = str(e)
        logger.error(f"Error indexing entity {entity_uuid}: {str(e)}")
        if profile_uuid:
            publish_event(profile_uuid, "entity_indexed", {
                "entity_uuid": entity_uuid,
                "section": entity_type,
                "status": "failed",
                "error": str(e),
            })
            publish_event(profile_uuid, "error", {"message": str(e), "entity_uuid": entity_uuid})

    finally:
        release_lock(f"entity:{entity_uuid}")
        session.close()

    return result
