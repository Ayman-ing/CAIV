"""Indexing router — profile indexing, per-entity status, per-entity reindex, SSE events."""
import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import HTTPException
from core.redis_client import acquire_lock_async, release_lock_async, subscribe_events
from db.session import get_db
from features.auth.dependencies import get_current_user
from features.auth.service import AuthService as AuthSvc
from features.users.models import User
from features.profiles.models import Profile
from features.profiles.repository import ProfileRepository
from features.profiles.service import ProfileService
from features.indexing.models import Embedding
from features.indexing.text_formatter import TextFormatter
from features.indexing.tasks import index_profile_task, index_entity_task
from features.indexing.schemas import (
    EntityIndexingStatusItem,
    IndexingStatusResponse,
    EntityIndexingResponse,
)
from shared.models.entity import Entity

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/profiles", tags=["indexing"])


async def get_profile_service(db: AsyncSession = Depends(get_db)) -> ProfileService:
    repository = ProfileRepository(db)
    return ProfileService(repository)


async def _auth_user_from_request(request: Request, token_qp: str | None, db: AsyncSession) -> User:
    raw = token_qp
    if not raw:
        auth_header = request.headers.get("authorization", "")
        raw = auth_header.removeprefix("Bearer ").strip()
    if not raw:
        raise HTTPException(status_code=401, message="Not authenticated")
    payload = AuthSvc.verify_token(raw)
    user_uuid = payload.get("sub")
    if not user_uuid:
        raise HTTPException(status_code=401, message="Invalid token")
    auth_svc = AuthSvc(db)
    user = await auth_svc.get_user_by_uuid(user_uuid)
    if not user:
        raise HTTPException(status_code=401, message="User not found")
    return user


ENTITY_TYPE_MAP: dict[str, tuple[type, callable, str]] = {}

for model_cls, text_fn, section_name in TextFormatter.get_sections_config():
    identity = getattr(model_cls, '__mapper_args__', {}).get('polymorphic_identity')
    if identity:
        ENTITY_TYPE_MAP[identity] = (model_cls, text_fn, section_name)

logger.debug(f"Built entity type map: {list(ENTITY_TYPE_MAP.keys())}")


async def _get_profile_entities(db: AsyncSession, profile_uuid: str) -> list[Entity]:
    profile_result = await db.execute(
        select(Profile).where(Profile.uuid == profile_uuid)
    )
    profile = profile_result.scalars().first()
    if not profile:
        return []

    profile_id = profile.id
    all_entities: list[Entity] = []

    for model_cls, _text_fn, _section_name in TextFormatter.get_sections_config():
        items = await db.execute(
            select(model_cls).where(model_cls.profile_id == profile_id)
        )
        for item in items.scalars().all():
            all_entities.append(item)

    return all_entities


async def _get_indexed_at_map(db: AsyncSession, entity_uuids: list[str]) -> dict[str, datetime]:
    if not entity_uuids:
        return {}

    from sqlalchemy.dialects.postgresql import UUID as PG_UUID
    import uuid as py_uuid

    uuids = [py_uuid.UUID(eid) for eid in entity_uuids]

    result = await db.execute(
        select(
            Embedding.entity_uuid,
            func.max(Embedding.indexed_at).label("max_indexed_at"),
        ).where(
            Embedding.entity_uuid.in_(uuids),
            Embedding.indexed_at.isnot(None),
        ).group_by(Embedding.entity_uuid)
    )

    return {str(row.entity_uuid): row.max_indexed_at for row in result.all()}


class IndexingResponse(BaseModel):
    task_id: str
    message: str
    profile_uuid: str
    status: str


@router.post("/{profile_uuid}/index", response_model=IndexingResponse, status_code=202)
async def index_profile(
    user_uuid: str,
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot index another user's profile")

    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot index another user's profile")

    profile = await service.get_profile_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")

    try:
        locked = await acquire_lock_async(profile_uuid, "pending")
        if not locked:
            logger.warning(f"Concurrent indexing rejected for profile {profile_uuid}")
            raise HTTPException(
                status_code=409,
                message="Indexing already in progress for this profile"
            )

        task = index_profile_task.delay(profile_uuid)

        logger.info(
            f"Indexing triggered for profile {profile_uuid} "
            f"(user {user_uuid}) → task_id={task.id}"
        )
        return IndexingResponse(
            task_id=task.id,
            message="Profile indexing started successfully",
            profile_uuid=profile_uuid,
            status="pending"
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start indexing for profile {profile_uuid}: {str(e)}")
        await release_lock_async(profile_uuid)
        raise HTTPException(status_code=500, message=f"Failed to start indexing: {str(e)}")


@router.get("/{profile_uuid}/indexing-status", response_model=IndexingStatusResponse)
async def get_indexing_status(
    profile_uuid: str,
    user_uuid: str = Query(...),
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
    db: AsyncSession = Depends(get_db),
):
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    profile = await service.get_profile_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")

    entities = await _get_profile_entities(db, profile_uuid)
    entity_uuids = [str(e.uuid) for e in entities]
    indexed_at_map = await _get_indexed_at_map(db, entity_uuids)

    items: list[EntityIndexingStatusItem] = []
    indexed_count = 0
    needs_reindex_count = 0
    never_indexed_count = 0
    all_indexed_ats: list[datetime] = []

    for entity in entities:
        e_uuid = str(entity.uuid)
        e_type = entity.entity_type
        updated_at = entity.updated_at
        indexed_at = indexed_at_map.get(e_uuid)

        if indexed_at is None:
            status = "never_indexed"
            needs_reindex = True
            never_indexed_count += 1
        elif indexed_at >= updated_at:
            status = "indexed"
            needs_reindex = False
            indexed_count += 1
            all_indexed_ats.append(indexed_at)
        else:
            status = "needs_reindex"
            needs_reindex = True
            needs_reindex_count += 1
            if indexed_at:
                all_indexed_ats.append(indexed_at)

        items.append(EntityIndexingStatusItem(
            uuid=e_uuid,
            entity_type=e_type,
            updated_at=updated_at,
            indexed_at=indexed_at,
            needs_reindex=needs_reindex,
            status=status,
        ))

    profile_indexed_at = max(all_indexed_ats) if all_indexed_ats else None

    return IndexingStatusResponse(
        profile_uuid=profile_uuid,
        entities=items,
        profile_indexed_at=profile_indexed_at,
        total_entities=len(items),
        indexed_count=indexed_count,
        needs_reindex_count=needs_reindex_count,
        never_indexed_count=never_indexed_count,
    )


@router.post("/{profile_uuid}/entities/{entity_uuid}/index", response_model=EntityIndexingResponse, status_code=202)
async def index_single_entity(
    profile_uuid: str,
    entity_uuid: str,
    user_uuid: str = Query(...),
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service),
    db: AsyncSession = Depends(get_db),
):
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    import uuid as py_uuid
    entity_result = await db.execute(
        select(Entity).where(Entity.uuid == py_uuid.UUID(entity_uuid))
    )
    entity = entity_result.scalars().first()
    if not entity:
        raise HTTPException(status_code=404, message="Entity not found")

    indexed_at_result = await db.execute(
        select(func.max(Embedding.indexed_at)).where(
            Embedding.entity_uuid == py_uuid.UUID(entity_uuid),
        )
    )
    max_indexed_at = indexed_at_result.scalar()
    if max_indexed_at and max_indexed_at >= entity.updated_at:
        raise HTTPException(
            status_code=400,
            message="Entity is already indexed — no changes detected"
        )

    entity_type = entity.entity_type

    model_info = ENTITY_TYPE_MAP.get(entity_type)
    if not model_info:
        raise HTTPException(status_code=400, message=f"Entity type '{entity_type}' cannot be indexed")

    model_cls, text_formatter_fn, _section_name = model_info

    full_entity = await db.execute(
        select(model_cls).where(model_cls.uuid == py_uuid.UUID(entity_uuid))
    )
    full_entity = full_entity.scalars().first()
    if not full_entity:
        raise HTTPException(status_code=404, message="Entity record not found")

    text = text_formatter_fn(full_entity)
    if not text or not text.strip():
        raise HTTPException(status_code=400, message="Entity has no indexable content")

    lock_key = f"entity:{entity_uuid}"
    locked = await acquire_lock_async(lock_key, "pending")
    if not locked:
        raise HTTPException(
            status_code=409,
            message="Indexing already in progress for this entity"
        )

    try:
        task = index_entity_task.delay(entity_uuid, entity_type, text, profile_uuid=profile_uuid)
        logger.info(
            f"Single entity indexing triggered: {entity_uuid} "
            f"({entity_type}) → task_id={task.id}"
        )
        return EntityIndexingResponse(
            task_id=task.id,
            entity_uuid=entity_uuid,
            status="pending",
        )
    except Exception as e:
        await release_lock_async(lock_key)
        logger.error(f"Failed to start entity indexing: {e}")
        raise HTTPException(status_code=500, message=f"Failed to start indexing: {str(e)}")


@router.get("/{profile_uuid}/index/events")
async def index_events_sse(
    request: Request,
    profile_uuid: str,
    user_uuid: str = Query(...),
    token: str | None = Query(None),
    db: AsyncSession = Depends(get_db),
):
    current_user = await _auth_user_from_request(request, token, db)

    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    repo = ProfileRepository(db)
    service = ProfileService(repo)
    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot access another user's profile")

    return StreamingResponse(
        subscribe_events(profile_uuid),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
