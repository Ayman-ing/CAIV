"""
Resume Import Repository - Database operations for resume uploads
"""
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from uuid import UUID

from .models import UploadedResume


class ResumeImportRepository:
    """Repository for resume import operations"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_uploaded_resume(
        self,
        profile_id: int,
        user_id: int,
        filename: str,
        extracted_data: dict
    ) -> UploadedResume:
        """Create a new uploaded resume record"""
        uploaded_resume = UploadedResume(
            profile_id=profile_id,
            user_id=user_id,
            original_filename=filename,
            extracted_data=extracted_data,
            import_status="pending"
        )

        self.db.add(uploaded_resume)
        await self.db.commit()
        await self.db.refresh(uploaded_resume)
        return uploaded_resume

    async def get_uploaded_resume_by_uuid(self, resume_uuid: UUID) -> Optional[UploadedResume]:
        """Get uploaded resume by UUID with profile eagerly loaded"""
        result = await self.db.execute(
            select(UploadedResume)
            .options(selectinload(UploadedResume.profile))
            .where(UploadedResume.uuid == resume_uuid)
        )
        return result.scalars().first()

    async def get_uploaded_resume_by_id(self, resume_id: int) -> Optional[UploadedResume]:
        """Get uploaded resume by ID"""
        result = await self.db.execute(
            select(UploadedResume).where(UploadedResume.id == resume_id)
        )
        return result.scalars().first()

    async def get_resumes_by_profile(self, profile_id: int) -> List[UploadedResume]:
        """Get all uploaded resumes for a profile"""
        result = await self.db.execute(
            select(UploadedResume)
            .where(UploadedResume.profile_id == profile_id)
            .order_by(UploadedResume.created_at.desc())
        )
        return result.scalars().all()

    async def get_resumes_by_user(self, user_id: int) -> List[UploadedResume]:
        """Get all uploaded resumes for a user"""
        result = await self.db.execute(
            select(UploadedResume)
            .where(UploadedResume.user_id == user_id)
            .order_by(UploadedResume.created_at.desc())
        )
        return result.scalars().all()

    async def update_resume_status(self, resume: UploadedResume, status: str) -> UploadedResume:
        """Update the import status of a resume"""
        resume.import_status = status
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def update_extracted_data(self, resume: UploadedResume, extracted_data: dict) -> UploadedResume:
        """Update the extracted data for a resume"""
        resume.extracted_data = extracted_data
        await self.db.commit()
        await self.db.refresh(resume)
        return resume

    async def delete_uploaded_resume(self, resume: UploadedResume) -> None:
        """Delete an uploaded resume record"""
        await self.db.delete(resume)
        await self.db.commit()