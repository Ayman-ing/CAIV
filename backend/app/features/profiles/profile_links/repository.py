"""
User Link Repository

Handles all database operations for user links.
"""

from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from features.profiles.profile_links.models import ProfileLink
from features.profiles.profile_links.schemas import ProfileLinkCreate, ProfileLinkUpdate


class ProfileLinkRepository:
    """Repository for user link database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, link_data: ProfileLinkCreate) -> ProfileLink:
        """Create a new profile link"""
        db_link = ProfileLink(
            profile_id=profile_id,
            label=link_data.label,
            url=str(link_data.url),
            platform=link_data.platform,
            is_visible=link_data.is_visible
        )
        self.db.add(db_link)
        await self.db.commit()
        await self.db.refresh(db_link)
        return db_link
    
    async def get_by_uuid(self, link_uuid: str) -> Optional[ProfileLink]:
        """Get user link by UUID"""
        result = await self.db.execute(select(ProfileLink).where(ProfileLink.uuid == link_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[ProfileLink]:
        """Get all links for a profile, ordered by platform"""
        result = await self.db.execute(
            select(ProfileLink)
            .where(ProfileLink.profile_id == profile_id)
            .order_by(ProfileLink.platform)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_by_platform(self, profile_id: int, platform: str) -> Optional[ProfileLink]:
        """Get profile link by platform for a specific profile"""
        result = await self.db.execute(
            select(ProfileLink)
            .where(ProfileLink.profile_id == profile_id, ProfileLink.platform == platform)
        )
        return result.scalars().first()
    
    async def update(self, db_link: ProfileLink, link_update: ProfileLinkUpdate) -> ProfileLink:
        """Update an existing user link"""
        update_data = link_update.model_dump(exclude_unset=True)
        
        # Convert URL to string if provided
        if 'url' in update_data and update_data['url'] is not None:
            update_data['url'] = str(update_data['url'])
        
        for field, value in update_data.items():
            setattr(db_link, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_link)
        return db_link
    
    async def delete(self, db_link: ProfileLink) -> bool:
        """Delete a user link"""
        await self.db.delete(db_link)
        await self.db.commit()
        return True
