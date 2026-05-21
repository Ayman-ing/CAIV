from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import ProjectRepository
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from features.profiles.repository import ProfileRepository

class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repository = ProjectRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_project(self, profile_uuid: str, project_data: ProjectCreate) -> ProjectResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        project = await self.repository.create_with_profile_id(profile.id, project_data)
        return ProjectResponse.model_validate(project)
    
    async def get_project_by_uuid(self, project_uuid: str) -> Optional[ProjectResponse]:
        project = await self.repository.get_by_uuid(project_uuid)
        return ProjectResponse.model_validate(project) if project else None
    
    async def get_projects_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        projects = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [ProjectResponse.model_validate(p) for p in projects]
    
    async def update_project_by_uuid(self, project_uuid: str, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
        project = await self.repository.update_by_uuid(project_uuid, project_data)
        return ProjectResponse.model_validate(project) if project else None
    
    async def delete_project_by_uuid(self, project_uuid: str) -> bool:
        return await self.repository.delete_by_uuid(project_uuid)
