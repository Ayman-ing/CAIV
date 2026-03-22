from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import EducationService
from .schemas import EducationCreate, EducationUpdate, EducationResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/education", tags=["education"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's education")
    return profile

@router.post("/", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
def create_education(
    profile_uuid: str,
    education_data: EducationCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new education record for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = EducationService(db)
    try:
        return service.create_education(profile_uuid, education_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[EducationResponse])
def get_profile_education(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all education records for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = EducationService(db)
    return service.get_education_by_profile(profile_uuid)

@router.put("/{education_uuid}", response_model=EducationResponse)
def update_education(
    profile_uuid: str,
    education_uuid: str, 
    education_data: EducationUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update education information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = EducationService(db)
    education = service.update_education_by_uuid(education_uuid, education_data)
    if not education:
        raise HTTPException(status_code=404, message="Education record not found")
    return education

@router.delete("/{education_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(
    profile_uuid: str,
    education_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete an education record by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = EducationService(db)
    if not service.delete_education_by_uuid(education_uuid):
        raise HTTPException(status_code=404, message="Education record not found")
