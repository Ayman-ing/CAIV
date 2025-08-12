from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from .service import SkillService
from .schemas import SkillCreate, SkillUpdate, SkillResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/skills", tags=["skills"])

@router.post("/", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
def create_skill(
    user_id: int,
    profile_id: int,
    skill_data: SkillCreate, 
    db: Session = Depends(get_db)
):
    """Create a new skill for the specified profile"""
    service = SkillService(db)
    try:
        return service.create_skill(skill_data, profile_id=profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[SkillResponse])
def get_profile_skills(
    user_id: int,
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get all skills for the specified profile"""
    service = SkillService(db)
    return service.get_skills_by_profile(profile_id)

@router.get("/{skill_uuid}", response_model=SkillResponse)
def get_skill(
    user_id: int,
    profile_id: int,
    skill_uuid: str, 
    db: Session = Depends(get_db)
):
    """Get skill by UUID for the specified profile"""
    service = SkillService(db)
    skill = service.get_skill_by_uuid(skill_uuid)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.get("/user/{user_uuid}", response_model=List[SkillResponse])
def get_user_skills(user_uuid: str, category: str = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all skills for a specific user by user UUID, optionally filtered by category"""
    service = SkillService(db)
    if category:
        return service.get_user_skills_by_category(user_uuid, category)
    return service.get_user_skills_by_uuid(user_uuid, skip, limit)

@router.get("/", response_model=List[SkillResponse])
def list_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all skills with pagination"""
    service = SkillService(db)
    return service.list_skills(skip, limit)

@router.put("/{skill_uuid}", response_model=SkillResponse)
def update_skill(skill_uuid: str, skill_data: SkillUpdate, db: Session = Depends(get_db)):
    """Update skill information by UUID"""
    service = SkillService(db)
    skill = service.update_skill_by_uuid(skill_uuid, skill_data)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@router.delete("/{skill_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_skill(skill_uuid: str, db: Session = Depends(get_db)):
    """Delete a skill by UUID"""
    service = SkillService(db)
    if not service.delete_skill_by_uuid(skill_uuid):
        raise HTTPException(status_code=404, detail="Skill not found")
