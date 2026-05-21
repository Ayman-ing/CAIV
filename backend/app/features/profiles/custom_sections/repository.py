"""
Custom Section Repository

Handles all database operations for custom sections.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import CustomSection
from .schemas import CustomSectionCreate, CustomSectionUpdate


class CustomSectionRepository:
    """Repository for custom section database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, section_data: CustomSectionCreate) -> CustomSection:
        """Create a new custom section"""
        db_section = CustomSection(
            user_id=user_id,
            **section_data.model_dump()
        )
        self.db.add(db_section)
        await self.db.commit()
        await self.db.refresh(db_section)
        return db_section
    
    async def get_by_uuid(self, section_uuid: str) -> Optional[CustomSection]:
        """Get custom section by UUID"""
        result = await self.db.execute(select(CustomSection).where(CustomSection.uuid == section_uuid))
        return result.scalars().first()
    
    async def create_with_profile_id(self, profile_id: int, section_data: CustomSectionCreate) -> CustomSection:
        """Create a new custom section for a profile"""
        db_section = CustomSection(
            profile_id=profile_id,
            **section_data.model_dump()
        )
        self.db.add(db_section)
        await self.db.commit()
        await self.db.refresh(db_section)
        return db_section
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[CustomSection]:
        """Get all custom sections for a profile"""
        result = await self.db.execute(
            select(CustomSection)
            .where(CustomSection.profile_id == profile_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_user_sections(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CustomSection]:
        """Get all custom sections for a user, ordered by order_index"""
        result = await self.db.execute(
            select(CustomSection)
            .where(CustomSection.user_id == user_id)
            .order_by(CustomSection.order_index)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def update(self, db_section: CustomSection, section_update: CustomSectionUpdate) -> CustomSection:
        """Update an existing custom section"""
        update_data = section_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_section, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_section)
        return db_section
    
    async def delete(self, db_section: CustomSection) -> bool:
        """Delete a custom section"""
        await self.db.delete(db_section)
        await self.db.commit()
        return True
