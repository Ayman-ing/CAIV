from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import SkillService
from .schemas import SkillCreate, SkillUpdate, SkillResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/skills", tags=["skills"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's skills")
    return profile

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    profile_uuid: str,
    skill_data: SkillCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new skill for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    try:
        return service.create_skill(profile_uuid, skill_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[SkillResponse])
def get_profile_skills(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all skills for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    return service.get_skills_by_profile(profile_uuid)

@router.put("/{skill_uuid}", response_model=SkillResponse)
def update_skill(
    profile_uuid: str,
    skill_uuid: str, 
    skill_data: SkillUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update skill information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    skill = service.update_skill_by_uuid(skill_uuid, skill_data)
    if not skill:
        raise HTTPException(status_code=404, message="Skill not found")
    return skill

@router.delete("/{skill_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(
    profile_uuid: str,
    skill_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a skill by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = SkillService(db)
    if not service.delete_skill_by_uuid(skill_uuid):
        raise HTTPException(status_code=404, message="Skill not found")
