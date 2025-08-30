from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import EducationRepository
from .schemas import EducationCreate, EducationUpdate, EducationResponse
from features.users.repository import UserRepository

class EducationService:
    def __init__(self, db: Session):
        self.repository = EducationRepository(db)
        self.user_repository = UserRepository(db)
    
    def create_education(self, education_data: EducationCreate) -> EducationResponse:
        user = self.user_repository.get_by_uuid(education_data.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        education = self.repository.create_with_user_id(user.id, education_data)
        return EducationResponse.model_validate(education)
    
    def get_education_by_uuid(self, education_uuid: str) -> Optional[EducationResponse]:
        education = self.repository.get_by_uuid(education_uuid)
        return EducationResponse.model_validate(education) if education else None
    
    def get_user_education_by_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[EducationResponse]:
        education = self.repository.get_by_user_uuid(user_uuid, skip, limit)
        return [EducationResponse.model_validate(e) for e in education]
    
    def list_education(self, skip: int = 0, limit: int = 100) -> List[EducationResponse]:
        education = self.repository.get_all(skip, limit)
        return [EducationResponse.model_validate(e) for e in education]
    
    def update_education_by_uuid(self, education_uuid: str, education_data: EducationUpdate) -> Optional[EducationResponse]:
        education = self.repository.update_by_uuid(education_uuid, education_data)
        return EducationResponse.model_validate(education) if education else None
    
    def delete_education_by_uuid(self, education_uuid: str) -> bool:
        return self.repository.delete_by_uuid(education_uuid)
