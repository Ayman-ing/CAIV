"""
Language Repository

Handles all database operations for language skills.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from features.profiles.languages import Language
from features.profiles.languages.schemas import LanguageCreate, LanguageUpdate


class LanguageRepository:
    """Repository for language database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_profile_id(self, profile_id: int, language_data: LanguageCreate) -> Language:
        """Create a new language record for a profile"""
        db_language = Language(
            profile_id=profile_id,
            **language_data.model_dump()
        )
        self.db.add(db_language)
        self.db.commit()
        self.db.refresh(db_language)
        return db_language
    
    def get_by_uuid(self, language_uuid: str) -> Optional[Language]:
        """Get language by UUID"""
        return self.db.query(Language).filter(Language.uuid == language_uuid).first()
    
    def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Language]:
        """Get all languages for a profile, ordered by proficiency level (highest first)"""
        return (
            self.db.query(Language)
            .filter(Language.profile_id == profile_id)
            .order_by(Language.proficiency.desc()) # Note: assuming proficiency order logic
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_profile_and_language(self, profile_id: int, language_name: str) -> Optional[Language]:
        """Check if a language already exists for a profile"""
        return (
            self.db.query(Language)
            .filter(Language.profile_id == profile_id, Language.language == language_name)
            .first()
        )
    
    def update(self, db_language: Language, language_update: LanguageUpdate) -> Language:
        """Update an existing language record"""
        update_data = language_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_language, field, value)
        
        self.db.commit()
        self.db.refresh(db_language)
        return db_language
    
    def delete(self, db_language: Language) -> bool:
        """Delete a language record"""
        self.db.delete(db_language)
        self.db.commit()
        return True
