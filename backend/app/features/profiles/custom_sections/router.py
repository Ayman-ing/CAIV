from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import CustomSectionService
from .schemas import CustomSectionCreate, CustomSectionUpdate, CustomSectionResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/custom-sections", tags=["custom-sections"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's custom sections")
    return profile

@router.post("/", response_model=CustomSectionResponse, status_code=status.HTTP_201_CREATED)
def create_custom_section(
    profile_uuid: str,
    section_data: CustomSectionCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new custom section for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CustomSectionService(db)
    try:
        return service.create_custom_section(profile_uuid, section_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[CustomSectionResponse])
def get_profile_custom_sections(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all custom sections for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CustomSectionService(db)
    return service.get_sections_by_profile(profile_uuid)

@router.put("/{section_uuid}", response_model=CustomSectionResponse)
def update_custom_section(
    profile_uuid: str,
    section_uuid: str, 
    section_data: CustomSectionUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update custom section information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CustomSectionService(db)
    section = service.update_custom_section_by_uuid(section_uuid, section_data)
    if not section:
        raise HTTPException(status_code=404, message="Custom section not found")
    return section

@router.delete("/{section_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_custom_section(
    profile_uuid: str,
    section_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a custom section by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CustomSectionService(db)
    if not service.delete_custom_section_by_uuid(section_uuid):
        raise HTTPException(status_code=404, message="Custom section not found")
