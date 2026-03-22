from sqlalchemy.orm import Session
from typing import List, Optional
from features.profiles.professional_summaries.models import ProfessionalSummary
from features.profiles.professional_summaries.schemas import ProfessionalSummaryCreate, ProfessionalSummaryUpdate

class ProfessionalSummaryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_uuid(self, uuid: str) -> Optional[ProfessionalSummary]:
        return self.db.query(ProfessionalSummary).filter(ProfessionalSummary.uuid == uuid).first()

    def get_all_by_profile_id(self, profile_id: int) -> List[ProfessionalSummary]:
        return self.db.query(ProfessionalSummary).filter(ProfessionalSummary.profile_id == profile_id).all()

    def create(self, profile_id: int, data: ProfessionalSummaryCreate) -> ProfessionalSummary:
        # Check if this is the first summary for this profile
        existing_count = self.db.query(ProfessionalSummary).filter(
            ProfessionalSummary.profile_id == profile_id
        ).count()
        
        # First summary should be default
        is_default = existing_count == 0
        
        db_summary = ProfessionalSummary(
            profile_id=profile_id,
            title=data.title,
            content=data.content,
            is_default=is_default
        )
        self.db.add(db_summary)
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary

    def update(self, db_summary: ProfessionalSummary, data: ProfessionalSummaryUpdate) -> ProfessionalSummary:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_summary, key, value)
        
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary

    def delete(self, db_summary: ProfessionalSummary) -> bool:
        self.db.delete(db_summary)
        self.db.commit()
        return True

    def set_as_default(self, db_summary: ProfessionalSummary) -> ProfessionalSummary:
        """Set this summary as default and unset all others for the same profile"""
        # First, unset all other summaries for the same profile
        self.db.query(ProfessionalSummary).filter(
            ProfessionalSummary.profile_id == db_summary.profile_id,
            ProfessionalSummary.id != db_summary.id
        ).update({ProfessionalSummary.is_default: False})
        
        # Set this one as default
        db_summary.is_default = True
        self.db.commit()
        self.db.refresh(db_summary)
        return db_summary
