from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import SkillRepository
from .schemas import SkillCreate, SkillUpdate, SkillResponse
from features.users.repository import UserRepository

class SkillService:
    def __init__(self, db: Session):
        self.repository = SkillRepository(db)
        self.user_repository = UserRepository(db)
    
    def create_skill(self, skill_data: SkillCreate) -> SkillResponse:
        user = self.user_repository.get_by_uuid(skill_data.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        skill = self.repository.create_with_user_id(user.id, skill_data)
        return SkillResponse.model_validate(skill)
    
    def get_skill_by_uuid(self, skill_uuid: str) -> Optional[SkillResponse]:
        skill = self.repository.get_by_uuid(skill_uuid)
        return SkillResponse.model_validate(skill) if skill else None
    
    def get_user_skills_by_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[SkillResponse]:
        skills = self.repository.get_by_user_uuid(user_uuid, skip, limit)
        return [SkillResponse.model_validate(s) for s in skills]
    
    def get_user_skills_by_category(self, user_uuid: str, category: str) -> List[SkillResponse]:
        skills = self.repository.get_by_category(user_uuid, category)
        return [SkillResponse.model_validate(s) for s in skills]
    
    def list_skills(self, skip: int = 0, limit: int = 100) -> List[SkillResponse]:
        skills = self.repository.get_all(skip, limit)
        return [SkillResponse.model_validate(s) for s in skills]
    
    def update_skill_by_uuid(self, skill_uuid: str, skill_data: SkillUpdate) -> Optional[SkillResponse]:
        skill = self.repository.update_by_uuid(skill_uuid, skill_data)
        return SkillResponse.model_validate(skill) if skill else None
    
    def delete_skill_by_uuid(self, skill_uuid: str) -> bool:
        return self.repository.delete_by_uuid(skill_uuid)
