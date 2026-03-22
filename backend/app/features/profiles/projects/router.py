from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import ProjectService
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/projects", tags=["projects"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's projects")
    return profile

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    profile_uuid: str,
    project_data: ProjectCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new project for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    try:
        return service.create_project(profile_uuid, project_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[ProjectResponse])
def get_profile_projects(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all projects for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    return service.get_projects_by_profile(profile_uuid)

@router.put("/{project_uuid}", response_model=ProjectResponse)
def update_project(
    profile_uuid: str,
    project_uuid: str, 
    project_data: ProjectUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update project information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    project = service.update_project_by_uuid(project_uuid, project_data)
    if not project:
        raise HTTPException(status_code=404, message="Project not found")
    return project

@router.delete("/{project_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    profile_uuid: str,
    project_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a project by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    if not service.delete_project_by_uuid(project_uuid):
        raise HTTPException(status_code=404, message="Project not found")
