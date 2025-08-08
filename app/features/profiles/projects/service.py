from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import ProjectRepository
from .schemas import ProjectCreate, ProjectUpdate, ProjectResponse
from app.features.users.repository import UserRepository

class ProjectService:
    def __init__(self, db: Session):
        self.repository = ProjectRepository(db)
        self.user_repository = UserRepository(db)
    
    def create_project(self, project_data: ProjectCreate) -> ProjectResponse:
        user = self.user_repository.get_by_uuid(project_data.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        project = self.repository.create_with_user_id(user.id, project_data)
        return ProjectResponse.model_validate(project)
    
    def get_project_by_uuid(self, project_uuid: str) -> Optional[ProjectResponse]:
        project = self.repository.get_by_uuid(project_uuid)
        return ProjectResponse.model_validate(project) if project else None
    
    def get_user_projects_by_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        projects = self.repository.get_by_user_uuid(user_uuid, skip, limit)
        return [ProjectResponse.model_validate(p) for p in projects]
    
    def list_projects(self, skip: int = 0, limit: int = 100) -> List[ProjectResponse]:
        projects = self.repository.get_all(skip, limit)
        return [ProjectResponse.model_validate(p) for p in projects]
    
    def update_project_by_uuid(self, project_uuid: str, project_data: ProjectUpdate) -> Optional[ProjectResponse]:
        project = self.repository.update_by_uuid(project_uuid, project_data)
        return ProjectResponse.model_validate(project) if project else None
    
    def delete_project_by_uuid(self, project_uuid: str) -> bool:
        return self.repository.delete_by_uuid(project_uuid)
