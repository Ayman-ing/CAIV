"""
User Link Service

Business logic for user link management.
"""

from typing import List, Optional
from app.features.user_links.repository import UserLinkRepository
from app.features.user_links.schemas import UserLinkCreate, UserLinkUpdate, UserLinkResponse


class UserLinkService:
    """Service layer for user link business logic"""
    
    def __init__(self, repository: UserLinkRepository):
        self.repository = repository
    
    def create_link(self, user_id: int, link_data: UserLinkCreate) -> UserLinkResponse:
        """Create a new user link"""
        # Check if user already has a link for this platform
        existing_link = self.repository.get_by_platform(user_id, link_data.platform)
        if existing_link:
            raise ValueError(f"Link for platform '{link_data.platform}' already exists")
        
        db_link = self.repository.create(user_id, link_data)
        return UserLinkResponse.model_validate(db_link)
    
    def get_link_by_uuid(self, link_uuid: str) -> Optional[UserLinkResponse]:
        """Get user link by UUID"""
        db_link = self.repository.get_by_uuid(link_uuid)
        if not db_link:
            return None
        return UserLinkResponse.model_validate(db_link)
    
    def get_user_links(self, user_id: int, skip: int = 0, limit: int = 100) -> List[UserLinkResponse]:
        """Get all links for a user"""
        db_links = self.repository.get_user_links(user_id, skip, limit)
        return [UserLinkResponse.model_validate(link) for link in db_links]
    
    def update_link(self, link_uuid: str, link_update: UserLinkUpdate) -> Optional[UserLinkResponse]:
        """Update a user link"""
        db_link = self.repository.get_by_uuid(link_uuid)
        if not db_link:
            return None
        
        # If updating platform, check for duplicates
        if link_update.platform:
            existing_link = self.repository.get_by_platform(db_link.user_id, link_update.platform)
            if existing_link and existing_link.uuid != link_uuid:
                raise ValueError(f"Link for platform '{link_update.platform}' already exists")
        
        updated_link = self.repository.update(db_link, link_update)
        return UserLinkResponse.model_validate(updated_link)
    
    def delete_link(self, link_uuid: str) -> bool:
        """Delete a user link"""
        db_link = self.repository.get_by_uuid(link_uuid)
        if not db_link:
            return False
        
        return self.repository.delete(db_link)
    
    def check_link_ownership(self, link_uuid: str, user_id: int) -> bool:
        """Check if a link belongs to a specific user"""
        db_link = self.repository.get_by_uuid(link_uuid)
        return db_link is not None and db_link.user_id == user_id
