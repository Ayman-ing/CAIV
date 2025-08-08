"""
Language Repository

Handles all database operations for language skills.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from app.db.models.language import Language
from app.features.languages.schemas import LanguageCreate, LanguageUpdate


class LanguageRepository:
    """Repository for language database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, language_data: LanguageCreate) -> Language:
        """Create a new language record"""
        db_language = Language(
            user_id=user_id,
            **language_data.model_dump()
        )
        self.db.add(db_language)
        self.db.commit()
        self.db.refresh(db_language)
        return db_language
    
    def get_by_uuid(self, language_uuid: str) -> Optional[Language]:
        """Get language by UUID"""
        return self.db.query(Language).filter(Language.uuid == language_uuid).first()
    
    def get_user_languages(self, user_id: int, skip: int = 0, limit: int = 100) -> List[Language]:
        """Get all languages for a user, ordered by proficiency level (highest first)"""
        return (
            self.db.query(Language)
            .filter(Language.user_id == user_id)
            .order_by(Language.proficiency_level.desc())
            .offset(skip)
            .limit(limit)
            .all()
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
    
    def get_by_language_name(self, user_id: int, language_name: str) -> Optional[Language]:
        """Get a specific language by name for a user"""
        return (
            self.db.query(Language)
            .filter(Language.user_id == user_id, Language.language == language_name)
            .first()
        )
