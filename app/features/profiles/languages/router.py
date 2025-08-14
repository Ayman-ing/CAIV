"""
Language Router

FastAPI routes for language skills management.
"""

from typing import List
from fastapi import APIRouter, Depends, status, Query
from core.exceptions import HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.languages.repository import LanguageRepository
from features.profiles.languages.service import LanguageService
from features.profiles.languages.schemas import LanguageCreate, LanguageUpdate, LanguageResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/languages", tags=["languages"])


def get_language_service(db: Session = Depends(get_db)) -> LanguageService:
    """Dependency to get language service"""
    repository = LanguageRepository(db)
    return LanguageService(repository)


@router.post("/", response_model=LanguageResponse, status_code=201)
async def create_language(
    user_id: int,
    profile_id: int,
    language_data: LanguageCreate,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Create a new language skill for the specified profile"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, message="Cannot create language for another user")
    
    try:
        return service.create_language(profile_id, language_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=list[LanguageResponse])
async def get_profile_languages(
    user_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Get all languages for the specified profile"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, message="Cannot access another user's languages")
    
    return service.get_languages_by_profile(profile_id)

@router.get("/{language_uuid}", response_model=LanguageResponse)
async def get_language(
    user_id: int,
    profile_id: int,
    language_uuid: str,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Get a specific language by UUID"""
    language = service.get_language_by_uuid(language_uuid)
    if not language:
        raise HTTPException(status_code=404, message="Language not found")
    
    # Check ownership
    if not service.check_language_ownership(language_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to access this language")
    
    return language


@router.get("/user/{user_uuid}", response_model=List[LanguageResponse])
async def get_user_languages(
    user_uuid: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Get all languages for a specific user (UUID-based)"""
    # For now, users can only access their own languages
    # In the future, this could be extended for public profiles
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, message="Not authorized to access other users' languages")
    
    return service.get_user_languages(current_user.id, skip, limit)


@router.put("/{language_uuid}", response_model=LanguageResponse)
async def update_language(
    language_uuid: str,
    language_update: LanguageUpdate,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Update a language skill"""
    # Check ownership
    if not service.check_language_ownership(language_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to update this language")
    
    try:
        updated_language = service.update_language(language_uuid, language_update)
        if not updated_language:
            raise HTTPException(status_code=404, message="Language not found")
        return updated_language
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.delete("/{language_uuid}", status_code=204)
async def delete_language(
    language_uuid: str,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Delete a language skill"""
    # Check ownership
    if not service.check_language_ownership(language_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to delete this language")
    
    success = service.delete_language(language_uuid)
    if not success:
        raise HTTPException(status_code=404, message="Language not found")


@router.get("/user/{user_uuid}/count")
async def get_user_language_count(
    user_uuid: str,
    current_user: User = Depends(get_current_user),
    service: LanguageService = Depends(get_language_service)
):
    """Get count of languages for a user"""
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, message="Not authorized to access other users' data")
    
    count = service.get_user_language_count(current_user.id)
    return {"count": count}
