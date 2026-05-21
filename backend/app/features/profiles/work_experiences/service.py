from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import WorkExperienceRepository
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse
from features.profiles.repository import ProfileRepository

class WorkExperienceService:
    def __init__(self, db: AsyncSession):
        self.repository = WorkExperienceRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_work_experience(self, profile_uuid: str, work_exp_data: WorkExperienceCreate) -> WorkExperienceResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        work_exp = await self.repository.create_with_profile_id(profile.id, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp)
    
    async def get_work_experience_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperienceResponse]:
        work_exp = await self.repository.get_by_uuid(work_exp_uuid)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    async def get_work_experiences_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[WorkExperienceResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        work_experiences = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [WorkExperienceResponse.model_validate(we) for we in work_experiences]
    
    async def update_work_experience_by_uuid(self, work_exp_uuid: str, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperienceResponse]:
        work_exp = await self.repository.update_by_uuid(work_exp_uuid, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    async def delete_work_experience_by_uuid(self, work_exp_uuid: str) -> bool:
        return await self.repository.delete_by_uuid(work_exp_uuid)
