from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import WorkExperienceRepository
from .schemas import WorkExperienceCreate, WorkExperienceUpdate, WorkExperienceResponse
from features.profiles.repository import ProfileRepository

class WorkExperienceService:
    def __init__(self, db: Session):
        self.repository = WorkExperienceRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    def create_work_experience(self, profile_uuid: str, work_exp_data: WorkExperienceCreate) -> WorkExperienceResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        work_exp = self.repository.create_with_profile_id(profile.id, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp)
    
    def get_work_experience_by_uuid(self, work_exp_uuid: str) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.get_by_uuid(work_exp_uuid)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def get_work_experiences_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[WorkExperienceResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        work_experiences = self.repository.get_by_profile_id(profile.id, skip, limit)
        return [WorkExperienceResponse.model_validate(we) for we in work_experiences]
    
    def update_work_experience_by_uuid(self, work_exp_uuid: str, work_exp_data: WorkExperienceUpdate) -> Optional[WorkExperienceResponse]:
        work_exp = self.repository.update_by_uuid(work_exp_uuid, work_exp_data)
        return WorkExperienceResponse.model_validate(work_exp) if work_exp else None
    
    def delete_work_experience_by_uuid(self, work_exp_uuid: str) -> bool:
        return self.repository.delete_by_uuid(work_exp_uuid)
