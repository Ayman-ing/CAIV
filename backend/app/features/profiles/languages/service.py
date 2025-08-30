"""
Language Service

Business logic for language skills management.
"""

from typing import List, Optional
from features.profiles.languages.repository import LanguageRepository
from features.profiles.languages.schemas import LanguageCreate, LanguageUpdate, LanguageResponse
from features.profiles.languages.models import Language


class LanguageService:
    """Service layer for language business logic"""
    
    def __init__(self, repository: LanguageRepository):
        self.repository = repository
    
    def create_language(self, user_id: int, language_data: LanguageCreate) -> LanguageResponse:
        """Create a new language skill"""
        # Check if user already has this language
        existing_language = self.repository.get_by_language_name(
            user_id=user_id, 
            language_name=language_data.language
        )
        
        if existing_language:
            raise ValueError(f"Language '{language_data.language}' already exists for this user")
        
        db_language = self.repository.create(user_id, language_data)
        return LanguageResponse.model_validate(db_language)
    
    def get_language_by_uuid(self, language_uuid: str) -> Optional[LanguageResponse]:
        """Get language by UUID"""
        db_language = self.repository.get_by_uuid(language_uuid)
        if not db_language:
            return None
        return LanguageResponse.model_validate(db_language)
    
    def get_user_languages(self, user_id: int, skip: int = 0, limit: int = 100) -> List[LanguageResponse]:
        """Get all languages for a user"""
        db_languages = self.repository.get_user_languages(user_id, skip, limit)
        return [LanguageResponse.model_validate(lang) for lang in db_languages]
    
    def update_language(self, language_uuid: str, language_update: LanguageUpdate) -> Optional[LanguageResponse]:
        """Update a language skill"""
        db_language = self.repository.get_by_uuid(language_uuid)
        if not db_language:
            return None
        
        # If updating language name, check for duplicates
        if language_update.language:
            existing_language = self.repository.get_by_language_name(
                user_id=db_language.user_id,
                language_name=language_update.language
            )
            if existing_language and existing_language.uuid != language_uuid:
                raise ValueError(f"Language '{language_update.language}' already exists for this user")
        
        updated_language = self.repository.update(db_language, language_update)
        return LanguageResponse.model_validate(updated_language)
    
    def delete_language(self, language_uuid: str) -> bool:
        """Delete a language skill"""
        db_language = self.repository.get_by_uuid(language_uuid)
        if not db_language:
            return False
        
        return self.repository.delete(db_language)
    
    def get_user_language_count(self, user_id: int) -> int:
        """Get count of languages for a user"""
        languages = self.repository.get_user_languages(user_id, skip=0, limit=1000)
        return len(languages)
    
    def check_language_ownership(self, language_uuid: str, user_id: int) -> bool:
        """Check if a language belongs to a specific user"""
        db_language = self.repository.get_by_uuid(language_uuid)
        return db_language is not None and db_language.user_id == user_id
