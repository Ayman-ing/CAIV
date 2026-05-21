from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import ProjectService
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/projects", tags=["projects"])


async def check_profile_ownership(db: AsyncSession, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = await repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(
            status_code=403, message="Not authorized to access this profile's projects"
        )
    return profile


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(
    profile_uuid: str,
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new project for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    try:
        project = await service.create_project(profile_uuid, project_data)

        # Trigger async indexing
        # trigger_section_item_indexing(
        #     item_uuid=project.uuid,
        #     section_type="project",
        #     user_uuid=current_user.uuid,
        #     db=db,
        # )

        return project
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/", response_model=List[ProjectResponse])
async def get_profile_projects(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get all projects for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    return await service.get_projects_by_profile(profile_uuid)


@router.put("/{project_uuid}", response_model=ProjectResponse)
async def update_project(
    profile_uuid: str,
    project_uuid: str,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update project information by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    project = await service.update_project_by_uuid(project_uuid, project_data)
    if not project:
        raise HTTPException(status_code=404, message="Project not found")

    # Trigger async indexing
    # trigger_section_item_indexing(
    #     item_uuid=project.uuid,
    #     section_type="project",
    #     user_uuid=current_user.uuid,
    #     db=db,
    # )

    return project


@router.delete("/{project_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(
    profile_uuid: str,
    project_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a project by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProjectService(db)
    if not await service.delete_project_by_uuid(project_uuid):
        raise HTTPException(status_code=404, message="Project not found")
