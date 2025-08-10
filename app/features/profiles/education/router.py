from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from .service import EducationService
from .schemas import EducationCreate, EducationUpdate, EducationResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/education", tags=["education"])

@router.post("/", response_model=EducationResponse, status_code=status.HTTP_201_CREATED)
def create_education(
    user_id: int,
    profile_id: int,
    education_data: EducationCreate, 
    db: Session = Depends(get_db)
):
    """Create a new education record for the specified profile"""
    service = EducationService(db)
    try:
        return service.create_education(education_data, profile_id=profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[EducationResponse])
def get_profile_education(
    user_id: int,
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get all education records for the specified profile"""
    service = EducationService(db)
    return service.get_education_by_profile(profile_id)

@router.get("/{education_uuid}", response_model=EducationResponse)
def get_education(
    user_id: int,
    profile_id: int,
    education_uuid: str, 
    db: Session = Depends(get_db)
):
    """Get education by UUID for the specified profile"""
    service = EducationService(db)
    education = service.get_education_by_uuid(education_uuid)
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    return education

@router.get("/user/{user_uuid}", response_model=List[EducationResponse])
def get_user_education(user_uuid: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all education records for a specific user by user UUID (ordered by end date desc)"""
    service = EducationService(db)
    return service.get_user_education_by_uuid(user_uuid, skip, limit)

@router.get("/", response_model=List[EducationResponse])
def list_education(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all education records with pagination"""
    service = EducationService(db)
    return service.list_education(skip, limit)

@router.put("/{education_uuid}", response_model=EducationResponse)
def update_education(education_uuid: str, education_data: EducationUpdate, db: Session = Depends(get_db)):
    """Update education information by UUID"""
    service = EducationService(db)
    education = service.update_education_by_uuid(education_uuid, education_data)
    if not education:
        raise HTTPException(status_code=404, detail="Education record not found")
    return education

@router.delete("/{education_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_education(education_uuid: str, db: Session = Depends(get_db)):
    """Delete an education record by UUID"""
    service = EducationService(db)
    if not service.delete_education_by_uuid(education_uuid):
        raise HTTPException(status_code=404, detail="Education record not found")
