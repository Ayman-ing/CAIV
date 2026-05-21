"""
Language Repository

Handles all database operations for language skills.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.profiles.languages import Language
from features.profiles.languages.schemas import LanguageCreate, LanguageUpdate


class LanguageRepository:
    """Repository for language database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, language_data: LanguageCreate) -> Language:
        """Create a new language record for a profile"""
        db_language = Language(
            profile_id=profile_id,
            **language_data.model_dump()
        )
        self.db.add(db_language)
        await self.db.commit()
        await self.db.refresh(db_language)
        return db_language
    
    async def get_by_uuid(self, language_uuid: str) -> Optional[Language]:
        """Get language by UUID"""
        result = await self.db.execute(select(Language).where(Language.uuid == language_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Language]:
        """Get all languages for a profile, ordered by proficiency level (highest first)"""
        result = await self.db.execute(
            select(Language)
            .where(Language.profile_id == profile_id)
            .order_by(Language.proficiency.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_profile_and_language(self, profile_id: int, language_name: str) -> Optional[Language]:
        """Check if a language already exists for a profile"""
        result = await self.db.execute(
            select(Language)
            .where(Language.profile_id == profile_id, Language.language == language_name)
        )
        return result.scalars().first()
    
    async def update(self, db_language: Language, language_update: LanguageUpdate) -> Language:
        """Update an existing language record"""
        update_data = language_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_language, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_language)
        return db_language
    
    async def delete(self, db_language: Language) -> bool:
        """Delete a language record"""
        await self.db.delete(db_language)
        await self.db.commit()
        return True
