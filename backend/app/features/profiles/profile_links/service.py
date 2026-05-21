from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import ProfileLinkRepository
from .schemas import ProfileLinkCreate, ProfileLinkUpdate, ProfileLinkResponse
from features.profiles.repository import ProfileRepository

class ProfileLinkService:
    def __init__(self, db: AsyncSession):
        self.repository = ProfileLinkRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_link(self, profile_uuid: str, link_data: ProfileLinkCreate) -> ProfileLinkResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        link = await self.repository.create_with_profile_id(profile.id, link_data)
        return ProfileLinkResponse.model_validate(link)
    
    async def get_link_by_uuid(self, link_uuid: str) -> Optional[ProfileLinkResponse]:
        link = await self.repository.get_by_uuid(link_uuid)
        return ProfileLinkResponse.model_validate(link) if link else None
    
    async def get_links_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[ProfileLinkResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        links = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [ProfileLinkResponse.model_validate(link) for link in links]
    
    async def update_link_by_uuid(self, link_uuid: str, link_update: ProfileLinkUpdate) -> Optional[ProfileLinkResponse]:
        link = await self.repository.get_by_uuid(link_uuid)
        if not link:
            return None
        updated_link = await self.repository.update(link, link_update)
        return ProfileLinkResponse.model_validate(updated_link)
    
    async def delete_link_by_uuid(self, link_uuid: str) -> bool:
        link = await self.repository.get_by_uuid(link_uuid)
        if not link:
            return False
        return await self.repository.delete(link)
