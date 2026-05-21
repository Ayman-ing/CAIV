from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .models import WorkExperience
from .schemas import WorkExperienceCreate, WorkExperienceUpdate

class WorkExperienceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, work_exp_data: WorkExperienceCreate) -> WorkExperience:
        """Create a new work experience for a profile"""
        data_dict = work_exp_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        work_exp = WorkExperience(**data_dict)
        self.db.add(work_exp)
        await self.db.commit()
        await self.db.refresh(work_exp)
        return work_exp
    
    async def create(self, work_exp_data: WorkExperienceCreate) -> WorkExperience:
        work_exp = WorkExperience(**work_exp_data.model_dump())
        self.db.add(work_exp)
        await self.db.commit()
        await self.db.refresh(work_exp)
        return work_exp
    
    async def get_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperience]:
        result = await self.db.execute(select(WorkExperience).where(WorkExperience.uuid == work_exp_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        """Get all work experiences for a profile"""
        result = await self.db.execute(
            select(WorkExperience)
            .where(WorkExperience.profile_id == profile_id)
            .order_by(WorkExperience.start_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_id(self, work_exp_id: int) -> Optional[WorkExperience]:
        result = await self.db.execute(select(WorkExperience).where(WorkExperience.id == work_exp_id))
        return result.scalars().first()
    
    async def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        result = await self.db.execute(
            select(WorkExperience)
            .where(WorkExperience.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        result = await self.db.execute(select(WorkExperience).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_by_uuid(self, work_exp_uuid: str, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperience]:
        """Update a work experience by UUID"""
        work_exp = await self.get_by_uuid(work_exp_uuid)
        if work_exp:
            for field, value in work_exp_data.model_dump(exclude_unset=True).items():
                setattr(work_exp, field, value)
            await self.db.commit()
            await self.db.refresh(work_exp)
        return work_exp
    
    async def update(self, work_exp_id: int, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperience]:
        work_exp = await self.get_by_id(work_exp_id)
        if work_exp:
            for field, value in work_exp_data.model_dump(exclude_unset=True).items():
                setattr(work_exp, field, value)
            await self.db.commit()
            await self.db.refresh(work_exp)
        return work_exp
    
    async def delete_by_uuid(self, work_exp_uuid: str) -> bool:
        """Delete a work experience by UUID"""
        work_exp = await self.get_by_uuid(work_exp_uuid)
        if work_exp:
            await self.db.delete(work_exp)
            await self.db.commit()
            return True
        return False
    
    async def create_with_user_id(self, user_id: int, work_exp_data: WorkExperienceCreate) -> WorkExperience:
        # Convert to dict and replace user_uuid with user_id
        data_dict = work_exp_data.model_dump()
        data_dict.pop('user_uuid', None)  # Remove user_uuid if exists
        data_dict['user_id'] = user_id
        
        work_exp = WorkExperience(**data_dict)
        self.db.add(work_exp)
        await self.db.commit()
        await self.db.refresh(work_exp)
        return work_exp
    
    async def get_by_user_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        from features.users.models import User
        result = await self.db.execute(
            select(WorkExperience)
            .join(User)
            .where(User.uuid == user_uuid)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
