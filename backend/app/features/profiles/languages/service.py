from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import LanguageRepository
from .schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from features.profiles.repository import ProfileRepository

class LanguageService:
    def __init__(self, db: Session):
        self.repository = LanguageRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    def create_language(self, profile_uuid: str, language_data: LanguageCreate) -> LanguageResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        # Check if language already exists for this profile (case-insensitive)
        existing = self.repository.get_by_profile_and_language(profile.id, language_data.language)
        if existing:
            raise ValueError(f"Language '{language_data.language}' already exists for this profile")
        
        language = self.repository.create_with_profile_id(profile.id, language_data)
        return LanguageResponse.model_validate(language)
    
    def get_language_by_uuid(self, language_uuid: str) -> Optional[LanguageResponse]:
        language = self.repository.get_by_uuid(language_uuid)
        return LanguageResponse.model_validate(language) if language else None
    
    def get_languages_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[LanguageResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        languages = self.repository.get_by_profile_id(profile.id, skip, limit)
        return [LanguageResponse.model_validate(lang) for lang in languages]
    
    def update_language_by_uuid(self, language_uuid: str, language_data: LanguageUpdate) -> Optional[LanguageResponse]:
        language = self.repository.get_by_uuid(language_uuid)
        if not language:
            return None
        updated_language = self.repository.update(language, language_data)
        return LanguageResponse.model_validate(updated_language)
    
    def delete_language_by_uuid(self, language_uuid: str) -> bool:
        language = self.repository.get_by_uuid(language_uuid)
        if not language:
            return False
        return self.repository.delete(language)
