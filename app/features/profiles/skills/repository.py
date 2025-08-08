from sqlalchemy.orm import Session
from typing import Optional, List
from .models import Skill
from .schemas import SkillCreate, SkillUpdate

class SkillRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_user_id(self, user_id: int, skill_data: SkillCreate) -> Skill:
        data_dict = skill_data.model_dump()
        data_dict.pop('user_uuid', None)
        data_dict['user_id'] = user_id
        
        skill = Skill(**data_dict)
        self.db.add(skill)
        self.db.commit()
        self.db.refresh(skill)
        return skill
    
    def get_by_uuid(self, skill_uuid: str) -> Optional[Skill]:
        return self.db.query(Skill).filter(Skill.uuid == skill_uuid).first()
    
    def get_by_user_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[Skill]:
        from app.features.users.models import User
        return (self.db.query(Skill)
                .join(User)
                .filter(User.uuid == user_uuid)
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_by_category(self, user_uuid: str, category: str) -> List[Skill]:
        from app.features.users.models import User
        return (self.db.query(Skill)
                .join(User)
                .filter(User.uuid == user_uuid, Skill.category == category)
                .all())
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Skill]:
        return self.db.query(Skill).offset(skip).limit(limit).all()
    
    def update_by_uuid(self, skill_uuid: str, skill_data: SkillUpdate) -> Optional[Skill]:
        skill = self.get_by_uuid(skill_uuid)
        if skill:
            for field, value in skill_data.model_dump(exclude_unset=True).items():
                setattr(skill, field, value)
            self.db.commit()
            self.db.refresh(skill)
        return skill
    
    def delete_by_uuid(self, skill_uuid: str) -> bool:
        skill = self.get_by_uuid(skill_uuid)
        if skill:
            self.db.delete(skill)
            self.db.commit()
            return True
        return False
