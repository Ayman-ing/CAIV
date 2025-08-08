from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.dependencies import get_db
from .service import WorkExperienceService
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse

router = APIRouter(prefix="/work-experiences", tags=["work-experiences"])

@router.post("/", response_model=WorkExperienceResponse, status_code=status.HTTP_201_CREATED)
def create_work_experience(work_exp_data: WorkExperienceCreate, db: Session = Depends(get_db)):
    """Create a new work experience"""
    service = WorkExperienceService(db)
    return service.create_work_experience(work_exp_data)

@router.get("/{work_exp_uuid}", response_model=WorkExperienceResponse)
def get_work_experience(work_exp_uuid: str, db: Session = Depends(get_db)):
    """Get work experience by UUID"""
    service = WorkExperienceService(db)
    work_exp = service.get_work_experience_by_uuid(work_exp_uuid)
    if not work_exp:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return work_exp

@router.get("/user/{user_uuid}", response_model=List[WorkExperienceResponse])
def get_user_work_experiences(user_uuid: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all work experiences for a specific user by user UUID"""
    service = WorkExperienceService(db)
    return service.get_user_work_experiences_by_uuid(user_uuid, skip, limit)

@router.get("/", response_model=List[WorkExperienceResponse])
def list_work_experiences(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all work experiences with pagination"""
    service = WorkExperienceService(db)
    return service.list_work_experiences(skip, limit)

@router.put("/{work_exp_uuid}", response_model=WorkExperienceResponse)
def update_work_experience(work_exp_uuid: str, work_exp_data: WorkExperienceUpdate, db: Session = Depends(get_db)):
    """Update work experience information by UUID"""
    service = WorkExperienceService(db)
    work_exp = service.update_work_experience_by_uuid(work_exp_uuid, work_exp_data)
    if not work_exp:
        raise HTTPException(status_code=404, detail="Work experience not found")
    return work_exp

@router.delete("/{work_exp_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_work_experience(work_exp_uuid: str, db: Session = Depends(get_db)):
    """Delete a work experience by UUID"""
    service = WorkExperienceService(db)
    if not service.delete_work_experience_by_uuid(work_exp_uuid):
        raise HTTPException(status_code=404, detail="Work experience not found")
