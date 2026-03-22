from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import LanguageService
from .schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/languages", tags=["languages"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's languages")
    return profile

@router.post("/", response_model=LanguageResponse, status_code=status.HTTP_201_CREATED)
def create_language(
    profile_uuid: str,
    language_data: LanguageCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new language for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    try:
        return service.create_language(profile_uuid, language_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[LanguageResponse])
def get_profile_languages(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all languages for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    return service.get_languages_by_profile(profile_uuid)

@router.put("/{language_uuid}", response_model=LanguageResponse)
def update_language(
    profile_uuid: str,
    language_uuid: str, 
    language_data: LanguageUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update language information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    language = service.update_language_by_uuid(language_uuid, language_data)
    if not language:
        raise HTTPException(status_code=404, message="Language not found")
    return language

@router.delete("/{language_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_language(
    profile_uuid: str,
    language_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a language by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = LanguageService(db)
    if not service.delete_language_by_uuid(language_uuid):
        raise HTTPException(status_code=404, message="Language not found")
