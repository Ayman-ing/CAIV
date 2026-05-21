from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from features.profiles.professional_summaries.models import ProfessionalSummary
from features.profiles.professional_summaries.schemas import ProfessionalSummaryCreate, ProfessionalSummaryUpdate

class ProfessionalSummaryRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_uuid(self, uuid: str) -> Optional[ProfessionalSummary]:
        result = await self.db.execute(select(ProfessionalSummary).where(ProfessionalSummary.uuid == uuid))
        return result.scalars().first()

    async def get_all_by_profile_id(self, profile_id: int) -> List[ProfessionalSummary]:
        result = await self.db.execute(select(ProfessionalSummary).where(ProfessionalSummary.profile_id == profile_id))
        return result.scalars().all()

    async def create(self, profile_id: int, data: ProfessionalSummaryCreate) -> ProfessionalSummary:
        # Check if this is the first summary for this profile
        result = await self.db.execute(
            select(ProfessionalSummary).where(ProfessionalSummary.profile_id == profile_id)
        )
        existing_count = len(result.scalars().all())
        
        # First summary should be default
        is_default = existing_count == 0
        
        db_summary = ProfessionalSummary(
            profile_id=profile_id,
            title=data.title,
            content=data.content,
            is_default=is_default
        )
        self.db.add(db_summary)
        await self.db.commit()
        await self.db.refresh(db_summary)
        return db_summary

    async def update(self, db_summary: ProfessionalSummary, data: ProfessionalSummaryUpdate) -> ProfessionalSummary:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_summary, key, value)
        
        await self.db.commit()
        return db_summary

    async def delete(self, db_summary: ProfessionalSummary) -> bool:
        await self.db.delete(db_summary)
        await self.db.commit()
        return True

    async def set_as_default(self, db_summary: ProfessionalSummary) -> ProfessionalSummary:
        """Set this summary as default and unset all others for the same profile"""
        # First, unset all other summaries for the same profile
        await self.db.execute(
            update(ProfessionalSummary)
            .where(
                ProfessionalSummary.profile_id == db_summary.profile_id,
                ProfessionalSummary.id != db_summary.id
            )
            .values(is_default=False)
        )
        
        # Set this one as default
        db_summary.is_default = True
        await self.db.commit()
        await self.db.refresh(db_summary)
        return db_summary
