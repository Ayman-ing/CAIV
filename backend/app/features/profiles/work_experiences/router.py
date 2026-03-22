from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import WorkExperienceService
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/work-experiences", tags=["work-experiences"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's work experiences")
    return profile

@router.post("/", response_model=WorkExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_work_experience(
    profile_uuid: str,
    work_exp_data: WorkExperienceCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new work experience for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    try:
        return service.create_work_experience(profile_uuid, work_exp_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[WorkExperienceResponse])
def get_profile_work_experiences(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all work experiences for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    return service.get_work_experiences_by_profile(profile_uuid)

@router.put("/{work_exp_uuid}", response_model=WorkExperienceResponse)
def update_work_experience(
    profile_uuid: str,
    work_exp_uuid: str, 
    work_exp_data: WorkExperienceUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update work experience information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    work_exp = service.update_work_experience_by_uuid(work_exp_uuid, work_exp_data)
    if not work_exp:
        raise HTTPException(status_code=404, message="Work experience not found")
    return work_exp

@router.delete("/{work_exp_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_experience(
    profile_uuid: str,
    work_exp_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a work experience by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = WorkExperienceService(db)
    if not service.delete_work_experience_by_uuid(work_exp_uuid):
        raise HTTPException(status_code=404, message="Work experience not found")
