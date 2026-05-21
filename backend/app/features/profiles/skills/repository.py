from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .models import Skill
from .schemas import SkillCreate, SkillUpdate

class SkillRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, skill_data: SkillCreate) -> Skill:
        data_dict = skill_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        skill = Skill(**data_dict)
        self.db.add(skill)
        await self.db.commit()
        await self.db.refresh(skill)
        return skill
    
    async def get_by_uuid(self, skill_uuid: str) -> Optional[Skill]:
        result = await self.db.execute(select(Skill).where(Skill.uuid == skill_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Skill]:
        result = await self.db.execute(
            select(Skill)
            .where(Skill.profile_id == profile_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_category(self, user_uuid: str, category: str) -> List[Skill]:
        from features.users.models import User
        result = await self.db.execute(
            select(Skill)
            .join(User)
            .where(User.uuid == user_uuid, Skill.category == category)
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Skill]:
        result = await self.db.execute(select(Skill).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_by_uuid(self, skill_uuid: str, skill_data: SkillUpdate) -> Optional[Skill]:
        skill = await self.get_by_uuid(skill_uuid)
        if skill:
            for field, value in skill_data.model_dump(exclude_unset=True).items():
                setattr(skill, field, value)
            await self.db.commit()
            await self.db.refresh(skill)
        return skill
    
    async def delete_by_uuid(self, skill_uuid: str) -> bool:
        skill = await self.get_by_uuid(skill_uuid)
        if skill:
            await self.db.delete(skill)
            await self.db.commit()
            return True
        return False
