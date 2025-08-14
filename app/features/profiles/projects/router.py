from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from .service import ProjectService
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/projects", tags=["projects"])

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    user_id: int,
    profile_id: int,
    project_data: ProjectCreate, 
    db: Session = Depends(get_db)
):
    """Create a new project for the specified profile"""
    service = ProjectService(db)
    try:
        return service.create_project(project_data, profile_id=profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=list[ProjectResponse])
def get_profile_projects(
    user_id: int,
    profile_id: int,
    db: Session = Depends(get_db)
):
    """Get all projects for the specified profile"""
    service = ProjectService(db)
    return service.get_projects_by_profile(profile_id)

@router.get("/{project_uuid}", response_model=ProjectResponse)
def get_project(
    user_id: int,
    profile_id: int,
    project_uuid: str, 
    db: Session = Depends(get_db)
):
    """Get project by UUID for the specified profile"""
    service = ProjectService(db)
    project = service.get_project_by_uuid(project_uuid)
    if not project:
        raise HTTPException(status_code=404, message="Project not found")
    return project

@router.get("/user/{user_uuid}", response_model=List[ProjectResponse])
def get_user_projects(user_uuid: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all projects for a specific user by user UUID"""
    service = ProjectService(db)
    return service.get_user_projects_by_uuid(user_uuid, skip, limit)

@router.get("/", response_model=List[ProjectResponse])
def list_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all projects with pagination"""
    service = ProjectService(db)
    return service.list_projects(skip, limit)

@router.put("/{project_uuid}", response_model=ProjectResponse)
def update_project(project_uuid: str, project_data: ProjectUpdate, db: Session = Depends(get_db)):
    """Update project information by UUID"""
    service = ProjectService(db)
    project = service.update_project_by_uuid(project_uuid, project_data)
    if not project:
        raise HTTPException(status_code=404, message="Project not found")
    return project

@router.delete("/{project_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_uuid: str, db: Session = Depends(get_db)):
    """Delete a project by UUID"""
    service = ProjectService(db)
    if not service.delete_project_by_uuid(project_uuid):
        raise HTTPException(status_code=404, message="Project not found")
