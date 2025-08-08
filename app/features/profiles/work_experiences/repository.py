from sqlalchemy.orm import Session
from typing import Optional, List
from .models import WorkExperience
from .schemas import WorkExperienceCreate, WorkExperienceUpdate

class WorkExperienceRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, work_exp_data: WorkExperienceCreate) -> WorkExperience:
        work_exp = WorkExperience(**work_exp_data.model_dump())
        self.db.add(work_exp)
        self.db.commit()
        self.db.refresh(work_exp)
        return work_exp
    
    def get_by_id(self, work_exp_id: int) -> Optional[WorkExperience]:
        return self.db.query(WorkExperience).filter(WorkExperience.id == work_exp_id).first()
    
    def get_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperience]:
        return self.db.query(WorkExperience).filter(WorkExperience.uuid == work_exp_uuid).first()
    
    def get_by_user_id(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        return (self.db.query(WorkExperience)
                .filter(WorkExperience.user_id == user_id)
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        return self.db.query(WorkExperience).offset(skip).limit(limit).all()
    
    def update(self, work_exp_id: int, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperience]:
        work_exp = self.get_by_id(work_exp_id)
        if work_exp:
            for field, value in work_exp_data.model_dump(exclude_unset=True).items():
                setattr(work_exp, field, value)
            self.db.commit()
            self.db.refresh(work_exp)
        return work_exp
    
    def create_with_user_id(self, user_id: int, work_exp_data: WorkExperienceCreate) -> WorkExperience:
        # Convert to dict and replace user_uuid with user_id
        data_dict = work_exp_data.model_dump()
        data_dict.pop('user_uuid', None)  # Remove user_uuid if exists
        data_dict['user_id'] = user_id
        
        work_exp = WorkExperience(**data_dict)
        self.db.add(work_exp)
        self.db.commit()
        self.db.refresh(work_exp)
        return work_exp
    
    def get_by_user_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[WorkExperience]:
        from app.features.users.models import User
        return (self.db.query(WorkExperience)
                .join(User)
                .filter(User.uuid == user_uuid)
                .offset(skip)
                .limit(limit)
                .all())
    
    def update_by_uuid(self, work_exp_uuid: str, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperience]:
        work_exp = self.get_by_uuid(work_exp_uuid)
        if work_exp:
            for field, value in work_exp_data.model_dump(exclude_unset=True).items():
                setattr(work_exp, field, value)
            self.db.commit()
            self.db.refresh(work_exp)
        return work_exp
    
    def delete_by_uuid(self, work_exp_uuid: str) -> bool:
        work_exp = self.get_by_uuid(work_exp_uuid)
        if work_exp:
            self.db.delete(work_exp)
            self.db.commit()
            return True
        return False
