from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import LanguageRepository
from .schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from features.profiles.repository import ProfileRepository

class LanguageService:
    def __init__(self, db: AsyncSession):
        self.repository = LanguageRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_language(self, profile_uuid: str, language_data: LanguageCreate) -> LanguageResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        # Check if language already exists for this profile (case-insensitive)
        existing = await self.repository.get_by_profile_and_language(profile.id, language_data.language)
        if existing:
            raise ValueError(f"Language '{language_data.language}' already exists for this profile")
        
        language = await self.repository.create_with_profile_id(profile.id, language_data)
        return LanguageResponse.model_validate(language)
    
    async def get_language_by_uuid(self, language_uuid: str) -> Optional[LanguageResponse]:
        language = await self.repository.get_by_uuid(language_uuid)
        return LanguageResponse.model_validate(language) if language else None
    
    async def get_languages_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[LanguageResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        languages = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [LanguageResponse.model_validate(lang) for lang in languages]
    
    async def update_language_by_uuid(self, language_uuid: str, language_data: LanguageUpdate) -> Optional[LanguageResponse]:
        language = await self.repository.get_by_uuid(language_uuid)
        if not language:
            return None
        updated_language = await self.repository.update(language, language_data)
        return LanguageResponse.model_validate(updated_language)
    
    async def delete_language_by_uuid(self, language_uuid: str) -> bool:
        language = await self.repository.get_by_uuid(language_uuid)
        if not language:
            return False
        return await self.repository.delete(language)
