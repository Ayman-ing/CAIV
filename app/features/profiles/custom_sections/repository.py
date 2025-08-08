"""
Custom Section Repository

Handles all database operations for custom sections.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from .models import CustomSection
from .schemas import CustomSectionCreate, CustomSectionUpdate


class CustomSectionRepository:
    """Repository for custom section database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, section_data: CustomSectionCreate) -> CustomSection:
        """Create a new custom section"""
        db_section = CustomSection(
            user_id=user_id,
            **section_data.model_dump()
        )
        self.db.add(db_section)
        self.db.commit()
        self.db.refresh(db_section)
        return db_section
    
    def get_by_uuid(self, section_uuid: str) -> Optional[CustomSection]:
        """Get custom section by UUID"""
        return self.db.query(CustomSection).filter(CustomSection.uuid == section_uuid).first()
    
    def get_user_sections(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CustomSection]:
        """Get all custom sections for a user, ordered by order_index"""
        return (
            self.db.query(CustomSection)
            .filter(CustomSection.user_id == user_id)
            .order_by(CustomSection.order_index)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update(self, db_section: CustomSection, section_update: CustomSectionUpdate) -> CustomSection:
        """Update an existing custom section"""
        update_data = section_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_section, field, value)
        
        self.db.commit()
        self.db.refresh(db_section)
        return db_section
    
    def delete(self, db_section: CustomSection) -> bool:
        """Delete a custom section"""
        self.db.delete(db_section)
        self.db.commit()
        return True
