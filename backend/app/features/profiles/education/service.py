from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import EducationRepository
from .schemas import EducationCreate, EducationUpdate, EducationResponse
from features.profiles.repository import ProfileRepository

class EducationService:
    def __init__(self, db: AsyncSession):
        self.repository = EducationRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_education(self, profile_uuid: str, education_data: EducationCreate) -> EducationResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        education = await self.repository.create_with_profile_id(profile.id, education_data)
        return EducationResponse.model_validate(education)
    
    async def get_education_by_uuid(self, education_uuid: str) -> Optional[EducationResponse]:
        education = await self.repository.get_by_uuid(education_uuid)
        return EducationResponse.model_validate(education) if education else None
    
    async def get_education_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[EducationResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        education = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [EducationResponse.model_validate(e) for e in education]
    
    async def update_education_by_uuid(self, education_uuid: str, education_data: EducationUpdate) -> Optional[EducationResponse]:
        education = await self.repository.update_by_uuid(education_uuid, education_data)
        return EducationResponse.model_validate(education) if education else None
    
    async def delete_education_by_uuid(self, education_uuid: str) -> bool:
        return await self.repository.delete_by_uuid(education_uuid)
