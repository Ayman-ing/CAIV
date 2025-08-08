from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import WorkExperienceRepository
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse
from app.features.users.repository import UserRepository

class WorkExperienceService:
    def __init__(self, db: Session):
        self.repository = WorkExperienceRepository(db)
        self.user_repository = UserRepository(db)
    
    def create_work_experience(self, work_exp_data: WorkExperienceCreate) -> WorkExperienceResponse:
        # Convert user_uuid to user_id
        user = self.user_repository.get_by_uuid(work_exp_data.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        work_exp = self.repository.create_with_user_id(user.id, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp)
    
    def get_work_experience(self, work_exp_id: int) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.get_by_id(work_exp_id)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def get_work_experience_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.get_by_uuid(work_exp_uuid)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def get_user_work_experiences(self, user_id: int, skip: int = 0, limit: int = 100) -> List[WorkExperienceResponse]:
        work_experiences = self.repository.get_by_user_id(user_id, skip, limit)
        return [WorkExperienceResponse.model_validate(we) for we in work_experiences]
    
    def list_work_experiences(self, skip: int = 0, limit: int = 100) -> List[WorkExperienceResponse]:
        work_experiences = self.repository.get_all(skip, limit)
        return [WorkExperienceResponse.model_validate(we) for we in work_experiences]
    
    def update_work_experience(self, work_exp_id: int, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.update(work_exp_id, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def get_work_experience_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.get_by_uuid(work_exp_uuid)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def get_user_work_experiences_by_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[WorkExperienceResponse]:
        work_experiences = self.repository.get_by_user_uuid(user_uuid, skip, limit)
        return [WorkExperienceResponse.model_validate(we) for we in work_experiences]
    
    def update_work_experience_by_uuid(self, work_exp_uuid: str, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.update_by_uuid(work_exp_uuid, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def delete_work_experience_by_uuid(self, work_exp_uuid: str) -> bool:
        return self.repository.delete_by_uuid(work_exp_uuid)
