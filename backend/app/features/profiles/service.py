"""
Profile Service

Business logic for user profile management.
"""

from typing import Optional
from features.profiles.repository import ProfileRepository
from features.profiles.schemas import ProfileCreate, ProfileUpdate, ProfileResponse
import json


class ProfileService:
    """Service layer for profile business logic"""
    
    def __init__(self, repository: ProfileRepository):
        self.repository = repository
    
    def create_profile(self, user_id: int, profile_data: ProfileCreate) -> ProfileResponse:
        """Create a new profile"""
        # Check if user already has a profile
        existing_profile = self.repository.get_by_user_id(user_id)
        if existing_profile:
            raise ValueError("User already has a profile")
        
        db_profile = self.repository.create(user_id, profile_data)
        return self._convert_to_response(db_profile)
    
    def get_profile_by_uuid(self, profile_uuid: str) -> Optional[ProfileResponse]:
        """Get profile by UUID"""
        db_profile = self.repository.get_by_uuid(profile_uuid)
        if not db_profile:
            return None
        return self._convert_to_response(db_profile)
    
    def get_user_profile(self, user_id: int) -> Optional[ProfileResponse]:
        """Get profile for a user"""
        db_profile = self.repository.get_by_user_id(user_id)
        if not db_profile:
            return None
        return self._convert_to_response(db_profile)
    
    def update_profile(self, profile_uuid: str, profile_update: ProfileUpdate) -> Optional[ProfileResponse]:
        """Update a profile"""
        db_profile = self.repository.get_by_uuid(profile_uuid)
        if not db_profile:
            return None
        
        updated_profile = self.repository.update(db_profile, profile_update)
        return self._convert_to_response(updated_profile)
    
    def delete_profile(self, profile_uuid: str) -> bool:
        """Delete a profile"""
        db_profile = self.repository.get_by_uuid(profile_uuid)
        if not db_profile:
            return False
        
        return self.repository.delete(db_profile)
    
    def check_profile_ownership(self, profile_uuid: str, user_id: int) -> bool:
        """Check if a profile belongs to a specific user"""
        db_profile = self.repository.get_by_uuid(profile_uuid)
        return db_profile is not None and db_profile.user_id == user_id
    
    def _convert_to_response(self, db_profile) -> ProfileResponse:
        """Convert database model to response schema"""
        # Parse specializations JSON
        specializations = None
        if db_profile.specializations:
            try:
                specializations = json.loads(db_profile.specializations)
            except json.JSONDecodeError:
                specializations = []
        
        return ProfileResponse(
            uuid=db_profile.uuid,
            user_id=db_profile.user_id,
            headline=db_profile.headline,
            summary=db_profile.summary,
            specializations=specializations,
            career_objectives=db_profile.career_objectives,
            created_at=db_profile.created_at,
            updated_at=db_profile.updated_at
        )
