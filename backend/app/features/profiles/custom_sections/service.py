from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import CustomSectionRepository
from .schemas import CustomSectionCreate, CustomSectionUpdate, CustomSectionResponse
from features.profiles.repository import ProfileRepository

class CustomSectionService:
    def __init__(self, db: AsyncSession):
        self.repository = CustomSectionRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_custom_section(self, profile_uuid: str, section_data: CustomSectionCreate) -> CustomSectionResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        section = await self.repository.create_with_profile_id(profile.id, section_data)
        return CustomSectionResponse.model_validate(section)
    
    async def get_custom_section_by_uuid(self, section_uuid: str) -> Optional[CustomSectionResponse]:
        section = await self.repository.get_by_uuid(section_uuid)
        return CustomSectionResponse.model_validate(section) if section else None
    
    async def get_sections_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[CustomSectionResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        sections = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [CustomSectionResponse.model_validate(s) for s in sections]
    
    async def update_custom_section_by_uuid(self, section_uuid: str, section_data: CustomSectionUpdate) -> Optional[CustomSectionResponse]:
        section = await self.repository.get_by_uuid(section_uuid)
        if not section:
            return None
        updated_section = await self.repository.update(section, section_data)
        return CustomSectionResponse.model_validate(updated_section)
    
    async def delete_custom_section_by_uuid(self, section_uuid: str) -> bool:
        section = await self.repository.get_by_uuid(section_uuid)
        if not section:
            return False
        return await self.repository.delete(section)
