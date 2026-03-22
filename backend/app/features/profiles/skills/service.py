from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import SkillRepository
from .schemas import SkillCreate, SkillUpdate, SkillResponse
from features.profiles.repository import ProfileRepository

class SkillService:
    def __init__(self, db: Session):
        self.repository = SkillRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    def create_skill(self, profile_uuid: str, skill_data: SkillCreate) -> SkillResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        skill = self.repository.create_with_profile_id(profile.id, skill_data)
        return SkillResponse.model_validate(skill)
    
    def get_skill_by_uuid(self, skill_uuid: str) -> Optional[SkillResponse]:
        skill = self.repository.get_by_uuid(skill_uuid)
        return SkillResponse.model_validate(skill) if skill else None
    
    def get_skills_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[SkillResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        skills = self.repository.get_by_profile_id(profile.id, skip, limit)
        return [SkillResponse.model_validate(s) for s in skills]
    
    def update_skill_by_uuid(self, skill_uuid: str, skill_data: SkillUpdate) -> Optional[SkillResponse]:
        skill = self.repository.update_by_uuid(skill_uuid, skill_data)
        return SkillResponse.model_validate(skill) if skill else None
    
    def delete_skill_by_uuid(self, skill_uuid: str) -> bool:
        return self.repository.delete_by_uuid(skill_uuid)
