from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import EducationRepository
from .schemas import EducationCreate, EducationUpdate, EducationResponse
from features.profiles.repository import ProfileRepository

class EducationService:
    def __init__(self, db: Session):
        self.repository = EducationRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    def create_education(self, profile_uuid: str, education_data: EducationCreate) -> EducationResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        education = self.repository.create_with_profile_id(profile.id, education_data)
        return EducationResponse.model_validate(education)
    
    def get_education_by_uuid(self, education_uuid: str) -> Optional[EducationResponse]:
        education = self.repository.get_by_uuid(education_uuid)
        return EducationResponse.model_validate(education) if education else None
    
    def get_education_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[EducationResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        education = self.repository.get_by_profile_id(profile.id, skip, limit)
        return [EducationResponse.model_validate(e) for e in education]
    
    def update_education_by_uuid(self, education_uuid: str, education_data: EducationUpdate) -> Optional[EducationResponse]:
        education = self.repository.update_by_uuid(education_uuid, education_data)
        return EducationResponse.model_validate(education) if education else None
    
    def delete_education_by_uuid(self, education_uuid: str) -> bool:
        return self.repository.delete_by_uuid(education_uuid)
