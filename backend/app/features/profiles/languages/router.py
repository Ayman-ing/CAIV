from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import LanguageService
from .schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from features.profiles.repository import ProfileRepository
# from features.vector_embeddings.async_service import trigger_section_item_indexing

router = APIRouter(
    prefix="/api/v1/profiles/{profile_uuid}/languages", tags=["languages"]
)


async def check_profile_ownership(db: AsyncSession, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = await repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403, message="Not authorized to access this profile's languages"
        )
    return profile


@router.post("/", response_model=LanguageResponse, status_code=status.HTTP_201_CREATED)
async def create_language(
    profile_uuid: str,
    language_data: LanguageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new language for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    try:
        language = await service.create_language(profile_uuid, language_data)

        # Trigger async indexing
        # trigger_section_item_indexing(
        #     item_uuid=language.uuid,
        #     section_type="language",
        #     user_uuid=current_user.uuid,
        #     db=db,
        # )

        return language
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/", response_model=List[LanguageResponse])
async def get_profile_languages(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all languages for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    return await service.get_languages_by_profile(profile_uuid)


@router.put("/{language_uuid}", response_model=LanguageResponse)
async def update_language(
    profile_uuid: str,
    language_uuid: str,
    language_data: LanguageUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update language information by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    language = await service.update_language_by_uuid(language_uuid, language_data)
    if not language:
        raise HTTPException(status_code=404, message="Language not found")

    # Trigger async indexing
    # trigger_section_item_indexing(
    #     item_uuid=language.uuid,
    #     section_type="language",
    #     user_uuid=current_user.uuid,
    #     db=db,
    # )

    return language


@router.delete("/{language_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_language(
    profile_uuid: str,
    language_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a language by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    if not await service.delete_language_by_uuid(language_uuid):
        raise HTTPException(status_code=404, message="Language not found")
