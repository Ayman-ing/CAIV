from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .models import Education
from .schemas import EducationCreate, EducationUpdate

class EducationRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, education_data: EducationCreate) -> Education:
        data_dict = education_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        education = Education(**data_dict)
        self.db.add(education)
        await self.db.commit()
        await self.db.refresh(education)
        return education
    
    async def get_by_uuid(self, education_uuid: str) -> Optional[Education]:
        result = await self.db.execute(select(Education).where(Education.uuid == education_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Education]:
        result = await self.db.execute(
            select(Education)
            .where(Education.profile_id == profile_id)
            .order_by(Education.end_date.desc().nulls_first())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Education]:
        result = await self.db.execute(select(Education).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_by_uuid(self, education_uuid: str, education_data: EducationUpdate) -> Optional[Education]:
        education = await self.get_by_uuid(education_uuid)
        if education:
            for field, value in education_data.model_dump(exclude_unset=True).items():
                setattr(education, field, value)
            await self.db.commit()
            await self.db.refresh(education)
        return education
    
    async def delete_by_uuid(self, education_uuid: str) -> bool:
        education = await self.get_by_uuid(education_uuid)
        if education:
            await self.db.delete(education)
            await self.db.commit()
            return True
        return False
