from sqlalchemy.orm import Session
from typing import List, Optional
from features.profiles.repository import ProfileRepository
from features.profiles.professional_summaries.repository import ProfessionalSummaryRepository
from features.profiles.professional_summaries.schemas import ProfessionalSummaryCreate, ProfessionalSummaryUpdate, ProfessionalSummaryResponse

class ProfessionalSummaryService:
    def __init__(self, db: Session):
        self.repository = ProfessionalSummaryRepository(db)
        self.profile_repository = ProfileRepository(db)

    def get_all_by_profile_uuid(self, profile_uuid: str) -> List[ProfessionalSummaryResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")

        summaries = self.repository.get_all_by_profile_id(profile.id)
        return [ProfessionalSummaryResponse.model_validate(summary) for summary in summaries]

    def create(self, profile_uuid: str, data: ProfessionalSummaryCreate) -> ProfessionalSummaryResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")

        summary = self.repository.create(profile.id, data)
        return ProfessionalSummaryResponse.model_validate(summary)

    def update(self, summary_uuid: str, data: ProfessionalSummaryUpdate) -> Optional[ProfessionalSummaryResponse]:
        db_summary = self.repository.get_by_uuid(summary_uuid)
        if not db_summary:
            return None

        updated_summary = self.repository.update(db_summary, data)
        return ProfessionalSummaryResponse.model_validate(updated_summary)

    def delete(self, summary_uuid: str) -> bool:
        db_summary = self.repository.get_by_uuid(summary_uuid)
        if not db_summary:
            return False

        return self.repository.delete(db_summary)

    def set_as_default(self, summary_uuid: str) -> Optional[ProfessionalSummaryResponse]:
        """Set a professional summary as default for its profile"""
        db_summary = self.repository.get_by_uuid(summary_uuid)
        if not db_summary:
            return None

        updated_summary = self.repository.set_as_default(db_summary)
        return ProfessionalSummaryResponse.model_validate(updated_summary)
