from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import SkillService
from .schemas import SkillCreate, SkillUpdate, SkillResponse
from features.profiles.repository import ProfileRepository
# from features.vector_embeddings.async_service import trigger_section_item_indexing

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/skills", tags=["skills"])


async def check_profile_ownership(db: AsyncSession, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = await repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403, message="Not authorized to access this profile's skills"
        )
    return profile


@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(
    profile_uuid: str,
    skill_data: SkillCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new skill for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    try:
        skill = await service.create_skill(profile_uuid, skill_data)

        # Trigger async indexing (sparse-only for skills)
        # trigger_section_item_indexing(
        #     item_uuid=skill.uuid,
        #     section_type="skill",
        #     user_uuid=current_user.uuid,
        #     db=db,
        # )

        return skill
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/", response_model=List[SkillResponse])
async def get_profile_skills(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all skills for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    return await service.get_skills_by_profile(profile_uuid)


@router.put("/{skill_uuid}", response_model=SkillResponse)
async def update_skill(
    profile_uuid: str,
    skill_uuid: str,
    skill_data: SkillUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update skill information by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    skill = await service.update_skill_by_uuid(skill_uuid, skill_data)
    if not skill:
        raise HTTPException(status_code=404, message="Skill not found")

    # Trigger async indexing
    # trigger_section_item_indexing(
    #     item_uuid=skill.uuid,
    #     section_type="skill",
    #     user_uuid=current_user.uuid,
    #     db=db,
    # )

    return skill


@router.delete("/{skill_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(
    profile_uuid: str,
    skill_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a skill by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    if not await service.delete_skill_by_uuid(skill_uuid):
        raise HTTPException(status_code=404, message="Skill not found")
