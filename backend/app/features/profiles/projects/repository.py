from sqlalchemy.orm import Session
from typing import Optional, List
from .models import Project
from .schemas import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_user_id(self, user_id: int, project_data: ProjectCreate) -> Project:
        data_dict = project_data.model_dump()
        data_dict.pop('user_uuid', None)
        data_dict['user_id'] = user_id
        
        project = Project(**data_dict)
        self.db.add(project)
        self.db.commit()
        self.db.refresh(project)
        return project
    
    def get_by_uuid(self, project_uuid: str) -> Optional[Project]:
        return self.db.query(Project).filter(Project.uuid == project_uuid).first()
    
    def get_by_user_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[Project]:
        from features.users.models import User
        return (self.db.query(Project)
                .join(User)
                .filter(User.uuid == user_uuid)
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
