from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .models import Project
from .schemas import ProjectCreate, ProjectUpdate

class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, project_data: ProjectCreate) -> Project:
        data_dict = project_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        # Convert HttpUrl to string for database storage
        if data_dict.get('url'):
            data_dict['url'] = str(data_dict['url'])
        
        project = Project(**data_dict)
        self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def get_by_uuid(self, project_uuid: str) -> Optional[Project]:
        result = await self.db.execute(select(Project).where(Project.uuid == project_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Project]:
        result = await self.db.execute(
            select(Project)
            .where(Project.profile_id == profile_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Project]:
        result = await self.db.execute(select(Project).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_by_uuid(self, project_uuid: str, project_data: ProjectUpdate) -> Optional[Project]:
        project = await self.get_by_uuid(project_uuid)
        if project:
            update_data = project_data.model_dump(exclude_unset=True)
            # Convert HttpUrl to string for database storage
            if update_data.get('url'):
                update_data['url'] = str(update_data['url'])
            for field, value in update_data.items():
                setattr(project, field, value)
            await self.db.commit()
            await self.db.refresh(project)
        return project
    
    async def delete_by_uuid(self, project_uuid: str) -> bool:
        project = await self.get_by_uuid(project_uuid)
        if project:
            await self.db.delete(project)
            await self.db.commit()
            return True
        return False
