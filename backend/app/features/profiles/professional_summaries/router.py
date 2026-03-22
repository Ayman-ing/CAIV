from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import ProfessionalSummaryService
from .schemas import ProfessionalSummaryCreate, ProfessionalSummaryUpdate, ProfessionalSummaryResponse
from features.profiles.repository import ProfileRepository

# Define router with prefix attached to a specific profile UUID
router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/professional-summaries", tags=["professional-summaries"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's summaries")
    return profile

@router.get("/", response_model=List[ProfessionalSummaryResponse])
def get_professional_summaries(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all professional summaries for a profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProfessionalSummaryService(db)
    try:
        return service.get_all_by_profile_uuid(profile_uuid)
    except ValueError as e:
        raise HTTPException(status_code=404, message=str(e))

@router.post("/", response_model=ProfessionalSummaryResponse, status_code=status.HTTP_201_CREATED)
def create_professional_summary(
    profile_uuid: str,
    data: ProfessionalSummaryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new professional summary for a profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProfessionalSummaryService(db)
    try:
        return service.create(profile_uuid, data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.put("/{summary_uuid}", response_model=ProfessionalSummaryResponse)
def update_professional_summary(
    profile_uuid: str,
    summary_uuid: str,
    data: ProfessionalSummaryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a professional summary"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProfessionalSummaryService(db)
    updated = service.update(summary_uuid, data)
    if not updated:
        raise HTTPException(status_code=404, message="Professional summary not found")
    return updated

@router.patch("/{summary_uuid}/set-default", response_model=ProfessionalSummaryResponse)
def set_professional_summary_as_default(
    profile_uuid: str,
    summary_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Set a professional summary as default for the profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProfessionalSummaryService(db)
    updated = service.set_as_default(summary_uuid)
    if not updated:
        raise HTTPException(status_code=404, message="Professional summary not found")
    return updated

@router.delete("/{summary_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_professional_summary(
    profile_uuid: str,
    summary_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a professional summary"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProfessionalSummaryService(db)
    if not service.delete(summary_uuid):
        raise HTTPException(status_code=404, message="Professional summary not found")
