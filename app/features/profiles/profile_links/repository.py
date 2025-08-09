"""
User Link Repository

Handles all database operations for user links.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from features.profiles.profile_links.models import ProfileLink
from features.profiles.profile_links.schemas import ProfileLinkCreate, ProfileLinkUpdate


class ProfileLinkRepository:
    """Repository for user link database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, link_data: ProfileLinkCreate) -> ProfileLink:
        """Create a new user link"""
        db_link = ProfileLink(
            user_id=user_id,
            platform=link_data.platform,
            url=str(link_data.url)
        )
        self.db.add(db_link)
        self.db.commit()
        self.db.refresh(db_link)
        return db_link
    
    def get_by_uuid(self, link_uuid: str) -> Optional[ProfileLink]:
        """Get user link by UUID"""
        return self.db.query(ProfileLink).filter(ProfileLink.uuid == link_uuid).first()
    
    def get_user_links(self, user_id: int, skip: int = 0, limit: int = 100) -> List[ProfileLink]:
        """Get all links for a user, ordered by platform"""
        return (
            self.db.query(ProfileLink)
            .filter(ProfileLink.user_id == user_id)
            .order_by(ProfileLink.platform)
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_platform(self, user_id: int, platform: str) -> Optional[ProfileLink]:
        """Get user link by platform for a specific user"""
        return (
            self.db.query(ProfileLink)
            .filter(ProfileLink.user_id == user_id, ProfileLink.platform == platform)
            .first()
        )
    
    def update(self, db_link: ProfileLink, link_update: ProfileLinkUpdate) -> ProfileLink:
        """Update an existing user link"""
        update_data = link_update.model_dump(exclude_unset=True)
        
        # Convert URL to string if provided
        if 'url' in update_data and update_data['url'] is not None:
            update_data['url'] = str(update_data['url'])
        
        for field, value in update_data.items():
            setattr(db_link, field, value)
        
        self.db.commit()
        self.db.refresh(db_link)
        return db_link
    
    def delete(self, db_link: ProfileLink) -> bool:
        """Delete a user link"""
        self.db.delete(db_link)
        self.db.commit()
        return True
