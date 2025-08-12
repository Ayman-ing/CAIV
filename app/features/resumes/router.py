"""
Resume Router

FastAPI routes for resume and component management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db.session import get_db
from features.auth.dependencies import get_current_user
from ..users.models import User
from .repository import ResumeRepository
from .service import ResumeService
from .schemas import (
    GeneratedResumeCreate, GeneratedResumeUpdate, GeneratedResumeResponse,
    ResumeComponentCreate, ResumeComponentUpdate, ResumeComponentResponse
)

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/resumes", tags=["resumes"])


def get_resume_service(db: Session = Depends(get_db)) -> ResumeService:
    """Dependency to get resume service"""
    repository = ResumeRepository(db)
    return ResumeService(repository)


# Resume endpoints
@router.post("/", response_model=GeneratedResumeResponse, status_code=201)
async def create_resume(
    user_id: int,
    resume_data: GeneratedResumeCreate,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Create a new resume for the specified user"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot create resume for another user")
    
    try:
        return service.create_resume(user_id, resume_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[GeneratedResumeResponse])
async def get_user_resumes(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Get all resumes for the specified user"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's resumes")
    
    return service.get_user_resumes(user_id)

@router.get("/{resume_uuid}", response_model=GeneratedResumeResponse)
async def get_resume(
    user_id: int,
    resume_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Get a specific resume for the user"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's resume")
    """Get a specific resume by UUID with all components"""
    resume = service.get_resume_by_uuid(resume_uuid)
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    # Check ownership
    if not service.check_resume_ownership(resume_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
    
    return resume


@router.get("/user/{user_uuid}", response_model=List[GeneratedResumeResponse])
async def get_user_resumes(
    user_uuid: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Get all resumes for a specific user (UUID-based)"""
    # For now, users can only access their own resumes
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not authorized to access other users' resumes")
    
    return service.get_user_resumes(current_user.id, skip, limit)


@router.put("/{resume_uuid}", response_model=GeneratedResumeResponse)
async def update_resume(
    resume_uuid: str,
    resume_update: GeneratedResumeUpdate,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Update a resume"""
    # Check ownership
    if not service.check_resume_ownership(resume_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this resume")
    
    try:
        updated_resume = service.update_resume(resume_uuid, resume_update)
        if not updated_resume:
            raise HTTPException(status_code=404, detail="Resume not found")
        return updated_resume
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{resume_uuid}", status_code=204)
async def delete_resume(
    resume_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Delete a resume and all its components"""
    # Check ownership
    if not service.check_resume_ownership(resume_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this resume")
    
    success = service.delete_resume(resume_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Resume not found")


# Component endpoints
@router.post("/{resume_uuid}/components", response_model=ResumeComponentResponse, status_code=201)
async def create_component(
    resume_uuid: str,
    component_data: ResumeComponentCreate,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Create a new component for a resume"""
    # Check ownership
    if not service.check_resume_ownership(resume_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to modify this resume")
    
    component = service.create_component(resume_uuid, component_data)
    if not component:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return component


@router.get("/{resume_uuid}/components", response_model=List[ResumeComponentResponse])
async def get_resume_components(
    resume_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Get all components for a resume"""
    # Check ownership
    if not service.check_resume_ownership(resume_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this resume")
    
    components = service.get_resume_components(resume_uuid)
    if components is None:
        raise HTTPException(status_code=404, detail="Resume not found")
    
    return components


@router.get("/components/{component_uuid}", response_model=ResumeComponentResponse)
async def get_component(
    component_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Get a specific component by UUID"""
    component = service.get_component_by_uuid(component_uuid)
    if not component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    # Check ownership
    if not service.check_component_ownership(component_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this component")
    
    return component


@router.put("/components/{component_uuid}", response_model=ResumeComponentResponse)
async def update_component(
    component_uuid: str,
    component_update: ResumeComponentUpdate,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Update a resume component"""
    # Check ownership
    if not service.check_component_ownership(component_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this component")
    
    updated_component = service.update_component(component_uuid, component_update)
    if not updated_component:
        raise HTTPException(status_code=404, detail="Component not found")
    
    return updated_component


@router.delete("/components/{component_uuid}", status_code=204)
async def delete_component(
    component_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ResumeService = Depends(get_resume_service)
):
    """Delete a resume component"""
    # Check ownership
    if not service.check_component_ownership(component_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this component")
    
    success = service.delete_component(component_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Component not found")
