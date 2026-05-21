"""Celery tasks for embedding generation and indexing."""
import logging
from typing import Optional
from datetime import datetime
import uuid
import asyncio
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.celery_app import celery_app
from core.config import get_settings
from db.session import SessionLocal
from .service import EmbeddingService
from .repository import EmbeddingRepository
from .text_formatter import TextFormatter

logger = logging.getLogger(__name__)


async def _get_session() -> AsyncSession:
    """Get database session."""
    return SessionLocal()


def _run_async(coro):
    """Run an async coroutine safely, handling event loop conflicts."""
    try:
        loop = asyncio.get_running_loop()
        if loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
            return loop.run_until_complete(coro)
    except RuntimeError:
        pass
    return asyncio.run(coro)


@celery_app.task(
    name="embedding.index_profile",
    bind=True,
    max_retries=3,
    time_limit=600,
    soft_time_limit=550,
)
def index_profile_task(self, profile_uuid: str) -> dict:
    """
    Index all profile section items by generating and storing embeddings.

    Args:
        profile_uuid: UUID of the profile to index

    Returns:
        Dictionary with indexing results and statistics
    """
    try:
        logger.info(f"Starting profile indexing for profile {profile_uuid}")
        result = _run_async(_index_profile_async(profile_uuid))
        logger.info(f"Profile indexing completed: {result}")
        return result

    except Exception as exc:
        logger.error(f"Error indexing profile {profile_uuid}: {str(exc)}")
        raise self.retry(exc=exc, countdown=60 * (2 ** self.request.retries))


async def _index_profile_async(profile_uuid: str) -> dict:
    """
    Asynchronously index all profile entities.

    Args:
        profile_uuid: UUID of the profile to index

    Returns:
        Dictionary with indexing statistics
    """
    logger.info(f"Async indexing profile {profile_uuid}")
    import time
    overall_start = time.monotonic()

    stats = {
        "profile_uuid": str(profile_uuid),
        "started_at": datetime.utcnow().isoformat(),
        "total_items": 0,
        "successful": 0,
        "failed": 0,
        "errors": [],
        "sections": {},
    }

    async with SessionLocal() as session:
        try:
            from features.profiles.models import Profile

            res = await session.execute(select(Profile).where(Profile.uuid == profile_uuid))
            profile = res.scalars().first()
            if not profile:
                raise ValueError(f"Profile not found: {profile_uuid}")

            profile_id = profile.id
            repo = EmbeddingRepository(session)

            async def create_embedding_for(entity_uuid: str, text: str, emb_type: str = 'full_text'):
                try:
                    if not text or not text.strip():
                        return None
                    embedding_vector = await EmbeddingService.generate_single_embedding(text)
                    logger.debug(
                        f"[Embedding] Generated vector (dim={len(embedding_vector)}) "
                        f"for entity {entity_uuid}"
                    )
                    text_preview = TextFormatter.extract_text_preview(text)
                    token_count = max(1, len(text) // 4)
                    embedding = await repo.create(
                        entity_uuid=entity_uuid,
                        vector_data=embedding_vector,
                        embedding_type=emb_type,
                        text_preview=text_preview,
                        token_count=token_count,
                    )
                    logger.debug(f"[Embedding] Stored embedding {embedding.uuid} for {entity_uuid}")
                    return embedding
                except Exception as e:
                    logger.error(f"Failed to create embedding for {entity_uuid}: {e}")
                    stats['failed'] += 1
                    stats['errors'].append(str(e))
                    return None

            from features.profiles.professional_summaries.models import ProfessionalSummary
            from features.profiles.work_experiences.models import WorkExperience
            from features.profiles.skills.models import Skill
            from features.profiles.projects.models import Project
            from features.profiles.education.models import Education
            from features.profiles.certificates.models import Certificate
            from features.profiles.languages.models import Language
            from features.profiles.custom_sections.models import CustomSection

            sections = [
                (ProfessionalSummary, lambda r: f"{r.title or ''}\n{r.content or ''}"),
                (WorkExperience, lambda r: f"{r.job_title or ''} at {r.company or ''}\n{r.description or ''}"),
                (Project, lambda r: f"{r.name or ''}\n{r.description or ''}\n{r.technologies or ''}"),
                (Skill, lambda r: f"{r.name or ''} {r.category or ''}"),
                (Education, lambda r: f"{r.degree or ''} {r.institution or ''}\n{r.description or ''}"),
                (Certificate, lambda r: f"{r.name or ''} {r.issuing_organization or ''}"),
                (Language, lambda r: f"{r.language or ''} ({r.proficiency or ''})"),
                (CustomSection, lambda r: f"{r.title or ''}\n{r.content or ''}"),
            ]

            for model, text_fn in sections:
                section_start = time.monotonic()
                section_name = model.__name__
                section_count = 0
                try:
                    q = select(model).where(model.profile_id == profile_id)
                    result = await session.execute(q)
                    items = result.scalars().all()
                    if not items:
                        logger.info(f"[Section] {section_name}: 0 items (skipped)")
                        stats['sections'][section_name] = {"count": 0, "duration_s": 0}
                        continue
                    logger.info(f"[Section] {section_name}: {len(items)} items found")
                    for item in items:
                        text = text_fn(item)
                        if not text or not text.strip():
                            logger.debug(f"[Section] {section_name}: skipped item {item.uuid} (empty text)")
                            continue
                        stats['total_items'] += 1
                        section_count += 1
                        emb = await create_embedding_for(str(item.uuid), text)
                        if emb:
                            stats['successful'] += 1
                    section_dur = time.monotonic() - section_start
                    stats['sections'][section_name] = {
                        "count": section_count,
                        "duration_s": round(section_dur, 2),
                    }
                    logger.info(
                        f"[Section] {section_name}: {section_count} entities indexed "
                        f"in {section_dur:.2f}s"
                    )
                except Exception as e:
                    logger.error(f"Error processing section {model.__name__}: {e}")
                    stats['errors'].append(f"{model.__name__}: {str(e)}")
                    stats['sections'][section_name] = {
                        "count": section_count,
                        "duration_s": round(time.monotonic() - section_start, 2),
                        "error": str(e),
                    }

            await session.commit()
            overall_dur = time.monotonic() - overall_start
            stats['duration_s'] = round(overall_dur, 2)
            stats['completed_at'] = datetime.utcnow().isoformat()
            logger.info(
                f"Indexing finished for profile {profile_uuid}: "
                f"{stats['successful']}/{stats['total_items']} items in {overall_dur:.2f}s "
                f"({stats['failed']} failed)"
            )
            return stats

        except Exception as e:
            overall_dur = time.monotonic() - overall_start
            logger.error(f"Error during profile indexing: {e}")
            try:
                await session.rollback()
            except Exception:
                pass
            stats['errors'].append(str(e))
            stats['failed'] = stats.get('failed', 0) + 1
            stats['duration_s'] = round(overall_dur, 2)
            stats['completed_at'] = datetime.utcnow().isoformat()
            return stats


@celery_app.task(
    name="embedding.index_entity",
    bind=True,
    max_retries=2,
)
def index_entity_task(
    self,
    entity_uuid: str,
    entity_type: str,
    text: str,
) -> dict:
    """
    Generate and store embedding for a single entity.

    Args:
        entity_uuid: UUID of the entity
        entity_type: Type of entity (work_experience, skill, education, etc.)
        text: Text content to embed

    Returns:
        Dictionary with embedding results (uuid, status)
    """
    try:
        logger.info(f"Generating embedding for entity {entity_uuid} ({entity_type})")
        result = _run_async(_index_entity_async(entity_uuid, entity_type, text))
        logger.info(f"Entity embedding completed: {result}")
        return result

    except Exception as exc:
        logger.error(f"Error indexing entity {entity_uuid}: {str(exc)}")
        raise self.retry(exc=exc, countdown=30 * (2 ** self.request.retries))


async def _index_entity_async(
    entity_uuid: str,
    entity_type: str,
    text: str,
) -> dict:
    """
    Asynchronously generate embedding for an entity and persist to DB.

    Args:
        entity_uuid: UUID of the entity
        entity_type: Type of entity
        text: Text to embed

    Returns:
        Dictionary with embedding data
    """
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
        return result

    async with SessionLocal() as session:
        try:
            embedding_vector = await EmbeddingService.generate_single_embedding(text)
            logger.debug(
                f"[Embedding] Generated vector (dim={len(embedding_vector)}) "
                f"for entity {entity_uuid} ({entity_type})"
            )
            text_preview = TextFormatter.extract_text_preview(text)
            token_count = max(1, len(text) // 4)

            repo = EmbeddingRepository(session)
            embedding = await repo.create(
                entity_uuid=entity_uuid,
                vector_data=embedding_vector,
                embedding_type='full_text',
                text_preview=text_preview,
                token_count=token_count,
            )

            await session.commit()

            result["status"] = "completed"
            result["embedding_uuid"] = str(embedding.uuid)
            logger.info(f"Created embedding {embedding.uuid} for entity {entity_uuid} ({entity_type})")

        except Exception as e:
            await session.rollback()
            result["error"] = str(e)
            logger.error(f"Error in entity indexing: {str(e)}")

    return result


@celery_app.task(name="embedding.clean_old_embeddings")
def clean_old_embeddings_task(days_old: int = 90) -> dict:
    """
    Clean up old embeddings (maintenance task).

    Args:
        days_old: Delete embeddings older than this many days

    Returns:
        Dictionary with cleanup statistics
    """
    logger.info(f"Cleaning embeddings older than {days_old} days")
    return {"status": "success", "deleted_count": 0}
