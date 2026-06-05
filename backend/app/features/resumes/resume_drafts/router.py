from typing import List
from fastapi import APIRouter, Depends
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .repository import ResumeDraftRepository
from .service import ResumeDraftService
from .schemas import ResumeDraftCreate, ResumeDraftUpdate, ResumeDraftResponse

router = APIRouter(
    prefix="/api/v1/profiles/{profile_id}/resume-drafts",
    tags=["resume-drafts"],
)


async def get_draft_service(db: AsyncSession = Depends(get_db)) -> ResumeDraftService:
    repository = ResumeDraftRepository(db)
    return ResumeDraftService(repository)


async def verify_profile_ownership(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from features.profiles.repository import ProfileRepository
    profile_repo = ProfileRepository(db)
    profile = await profile_repo.get_by_uuid(profile_id)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile")
    return profile


@router.post("/", response_model=ResumeDraftResponse, status_code=201)
async def create_draft(
    profile_id: str,
    data: ResumeDraftCreate,
    current_user: User = Depends(get_current_user),
    service: ResumeDraftService = Depends(get_draft_service),
    profile=Depends(verify_profile_ownership),
):
    return await service.create_draft(profile.id, data)


@router.get("/", response_model=List[ResumeDraftResponse])
async def list_drafts(
    profile_id: str,
    current_user: User = Depends(get_current_user),
    service: ResumeDraftService = Depends(get_draft_service),
    profile=Depends(verify_profile_ownership),
):
    return await service.list_drafts(profile.id)


@router.get("/{draft_uuid}", response_model=ResumeDraftResponse)
async def get_draft(
    profile_id: str,
    draft_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeDraftService = Depends(get_draft_service),
    profile=Depends(verify_profile_ownership),
):
    draft = await service.get_draft(draft_uuid)
    if not draft:
        raise HTTPException(status_code=404, message="Draft not found")
    return draft


@router.put("/{draft_uuid}", response_model=ResumeDraftResponse)
async def update_draft(
    profile_id: str,
    draft_uuid: str,
    data: ResumeDraftUpdate,
    current_user: User = Depends(get_current_user),
    service: ResumeDraftService = Depends(get_draft_service),
    profile=Depends(verify_profile_ownership),
):
    draft = await service.update_draft(draft_uuid, data)
    if not draft:
        raise HTTPException(status_code=404, message="Draft not found")
    return draft


@router.delete("/{draft_uuid}", status_code=204)
async def delete_draft(
    profile_id: str,
    draft_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeDraftService = Depends(get_draft_service),
    profile=Depends(verify_profile_ownership),
):
    success = await service.delete_draft(draft_uuid)
    if not success:
        raise HTTPException(status_code=404, message="Draft not found")
