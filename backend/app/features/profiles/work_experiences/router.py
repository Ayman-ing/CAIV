from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import WorkExperienceService
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(
    prefix="/api/v1/profiles/{profile_uuid}/work-experiences", tags=["work-experiences"]
)


async def check_profile_ownership(db: AsyncSession, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = await repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403,
            message="Not authorized to access this profile's work experiences",
        )
    return profile


@router.post(
    "/", response_model=WorkExperienceResponse, status_code=status.HTTP_201_CREATED
)
async def create_work_experience(
    profile_uuid: str,
    work_exp_data: WorkExperienceCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new work experience for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    try:
        work_exp = await service.create_work_experience(profile_uuid, work_exp_data)

        # Trigger async indexing
        # trigger_section_item_indexing(
        #     item_uuid=work_exp.uuid,
        #     section_type="work_experience",
        #     user_uuid=current_user.uuid,
        #     db=db,
        # )

        return work_exp
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/", response_model=List[WorkExperienceResponse])
async def get_profile_work_experiences(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all work experiences for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    return await service.get_work_experiences_by_profile(profile_uuid)


@router.put("/{work_exp_uuid}", response_model=WorkExperienceResponse)
async def update_work_experience(
    profile_uuid: str,
    work_exp_uuid: str,
    work_exp_data: WorkExperienceUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update work experience information by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    work_exp = await service.update_work_experience_by_uuid(work_exp_uuid, work_exp_data)
    if not work_exp:
        raise HTTPException(status_code=404, message="Work experience not found")

    # Trigger async indexing
    # trigger_section_item_indexing(
    #     item_uuid=work_exp.uuid,
    #     section_type="work_experience",
    #     user_uuid=current_user.uuid,
    #     db=db,
    # )

    return work_exp


@router.delete("/{work_exp_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_work_experience(
    profile_uuid: str,
    work_exp_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a work experience by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    if not await service.delete_work_experience_by_uuid(work_exp_uuid):
        raise HTTPException(status_code=404, message="Work experience not found")
