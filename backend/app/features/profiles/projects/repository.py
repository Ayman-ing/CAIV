from sqlalchemy.orm import Session
from typing import Optional, List
from .models import Project
from .schemas import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_profile_id(self, profile_id: int, project_data: ProjectCreate) -> Project:
        data_dict = project_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        # Convert HttpUrl to string for database storage
        if data_dict.get('url'):
            data_dict['url'] = str(data_dict['url'])
        
        project = Project(**data_dict)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_uuid(self, project_uuid: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.uuid == project_uuid).first()
    
    def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        return (self.db.query(Project)
                .filter(Project.profile_id == profile_id)
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        return self.db.query(Project).offset(skip).limit(limit).all()
    
    def update_by_uuid(self, project_uuid: str, project_data: ProjectUpdate) -> Optional[Project]:
        project = self.get_by_uuid(project_uuid)
        if project:
            for field, value in project_data.model_dump(exclude_unset=True).items():
                setattr(project, field, value)
            self.db.commit()
            self.db.refresh(project)
        return project
    
    def delete_by_uuid(self, project_uuid: str) -> bool:
        project = self.get_by_uuid(project_uuid)
        if project:
            self.db.delete(project)
            self.db.commit()
            return True
        return False
