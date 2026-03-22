from sqlalchemy.orm import Session
from typing import Optional, List
from .models import Education
from .schemas import EducationCreate, EducationUpdate

class EducationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_profile_id(self, profile_id: int, education_data: EducationCreate) -> Education:
        data_dict = education_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        education = Education(**data_dict)
        self.db.add(education)
        self.db.commit()
        self.db.refresh(education)
        return education
    
    def get_by_uuid(self, education_uuid: str) -> Optional[Education]:
        return self.db.query(Education).filter(Education.uuid == education_uuid).first()
    
    def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Education]:
        return (self.db.query(Education)
                .filter(Education.profile_id == profile_id)
                .order_by(Education.end_date.desc().nulls_first())
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Education]:
        return self.db.query(Education).offset(skip).limit(limit).all()
    
    def update_by_uuid(self, education_uuid: str, education_data: EducationUpdate) -> Optional[Education]:
        education = self.get_by_uuid(education_uuid)
        if education:
            for field, value in education_data.model_dump(exclude_unset=True).items():
                setattr(education, field, value)
            self.db.commit()
            self.db.refresh(education)
        return education
    
    def delete_by_uuid(self, education_uuid: str) -> bool:
        education = self.get_by_uuid(education_uuid)
        if education:
            self.db.delete(education)
            self.db.commit()
            return True
        return False
