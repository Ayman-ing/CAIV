"""
User Link Service

Business logic for user link management.
"""

from typing import List, Optional
from features.profiles.profile_links.repository import ProfileLinkRepository
from features.profiles.profile_links.schemas import ProfileLinkCreate, ProfileLinkUpdate, ProfileLinkResponse


class ProfileLinkService:
    """Service layer for user link business logic"""
    
    def __init__(self, repository: ProfileLinkRepository):
        self.repository = repository
    
    def create_link(self, user_id: int, link_data: ProfileLinkCreate) -> ProfileLinkResponse:
        """Create a new user link"""
        # Check if user already has a link for this platform
        existing_link = self.repository.get_by_platform(user_id, link_data.platform)
        if existing_link:
            raise ValueError(f"Link for platform '{link_data.platform}' already exists")
        
        db_link = self.repository.create(user_id, link_data)
        return ProfileLinkResponse.model_validate(db_link)
    
    def get_link_by_uuid(self, link_uuid: str) -> Optional[ProfileLinkResponse]:
        """Get user link by UUID"""
        db_link = self.repository.get_by_uuid(link_uuid)
        if not db_link:
            return None
        return ProfileLinkResponse.model_validate(db_link)
    
    def get_user_links(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ProfileLinkResponse]:
        """Get all links for a user"""
        db_links = self.repository.get_user_links(user_id, skip, limit)
        return [ProfileLinkResponse.model_validate(link) for link in db_links]
    
    def update_link(self, link_uuid: str, link_update: ProfileLinkUpdate) -> Optional[ProfileLinkResponse]:
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
        return ProfileLinkResponse.model_validate(updated_link)
    
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
