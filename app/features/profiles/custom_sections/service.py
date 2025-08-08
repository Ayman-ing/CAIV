"""
Custom Section Service

Business logic for custom sections operations.
"""

from typing import List, Optional
from app.features.custom_sections.repository import CustomSectionRepository
from app.features.custom_sections.schemas import CustomSectionCreate, CustomSectionUpdate, CustomSectionResponse


class CustomSectionService:
    """Service layer for custom section operations"""
    
    def __init__(self, repository: CustomSectionRepository):
        self.repository = repository

    def create_custom_section(self, user_id: int, section_data: CustomSectionCreate) -> CustomSectionResponse:
        """Create a new custom section for a user"""
        # Check for duplicate titles for the same user
        existing_sections = self.repository.get_user_custom_sections(user_id)
        if any(section.title.lower() == section_data.title.lower() for section in existing_sections):
            raise ValueError(f"Custom section with title '{section_data.title}' already exists")
        
        db_section = self.repository.create(user_id, section_data)
        return CustomSectionResponse.from_orm(db_section)

    def get_custom_section_by_uuid(self, section_uuid: str) -> Optional[CustomSectionResponse]:
        """Get a custom section by UUID"""
        db_section = self.repository.get_by_uuid(section_uuid)
        return CustomSectionResponse.from_orm(db_section) if db_section else None

    def get_user_custom_sections(self, user_id: int, skip: int = 0, limit: int = 100) -> List[CustomSectionResponse]:
        """Get all custom sections for a user, ordered by order_index"""
        db_sections = self.repository.get_user_custom_sections(user_id, skip, limit)
        return [CustomSectionResponse.from_orm(section) for section in db_sections]

    def update_custom_section(self, section_uuid: str, section_update: CustomSectionUpdate) -> Optional[CustomSectionResponse]:
        """Update a custom section"""
        db_section = self.repository.get_by_uuid(section_uuid)
        if not db_section:
            return None
        
        # Check for duplicate titles if title is being updated
        if section_update.title:
            existing_sections = self.repository.get_user_custom_sections(db_section.user_id)
            for section in existing_sections:
                if section.id != db_section.id and section.title.lower() == section_update.title.lower():
                    raise ValueError(f"Custom section with title '{section_update.title}' already exists")
        
        updated_section = self.repository.update(db_section, section_update)
        if updated_section:
            return CustomSectionResponse.from_orm(updated_section)
        return None

    def delete_custom_section(self, section_uuid: str) -> bool:
        """Delete a custom section"""
        db_section = self.repository.get_by_uuid(section_uuid)
        if not db_section:
            return False
        return self.repository.delete(db_section)

    def check_custom_section_ownership(self, section_uuid: str, user_id: int) -> bool:
        """Check if a custom section belongs to a specific user"""
        db_section = self.repository.get_by_uuid(section_uuid)
        return db_section is not None and db_section.user_id == user_id
