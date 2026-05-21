"""
Profile Repository

Handles all database operations for user profiles.
"""

from typing import Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import Profile
from .schemas import ProfileCreate, ProfileUpdate


class ProfileRepository:
    """Repository for profile database operations"""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, profile_data: ProfileCreate) -> Profile:
        """Create a new profile"""
        db_profile = Profile(
            user_id=user_id,
            name=profile_data.name,
            email=profile_data.email,
            phone_number=profile_data.phone_number,
            location=profile_data.location
        )
        self.db.add(db_profile)
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    async def get_by_uuid(self, profile_uuid: str) -> Optional[Profile]:
        """Get profile by UUID"""
        result = await self.db.execute(select(Profile).where(Profile.uuid == profile_uuid))
        return result.scalars().first()
    
    async def get_by_user_id(self, user_id: int) -> Optional[Profile]:
        """Get profile by user ID (users should have only one profile)"""
        result = await self.db.execute(select(Profile).where(Profile.user_id == user_id))
        return result.scalars().first()
    
    async def update(self, db_profile: Profile, profile_update: ProfileUpdate) -> Profile:
        """Update an existing profile"""
        update_data = profile_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_profile, field, value)
        
        await self.db.commit()
        await self.db.refresh(db_profile)
        return db_profile
    
    async def delete(self, db_profile: Profile) -> bool:
        """Delete a profile"""
        await self.db.delete(db_profile)
        await self.db.commit()
        return True
