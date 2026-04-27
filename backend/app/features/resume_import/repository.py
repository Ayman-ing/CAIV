"""
Resume Import Repository - Database operations for resume uploads
"""
from sqlalchemy.orm import Session
from typing import Optional, List
from uuid import UUID

from .models import UploadedResume


class ResumeImportRepository:
    """Repository for resume import operations"""

    def __init__(self, db: Session):
        self.db = db

    def create_uploaded_resume(
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
        self.db.commit()
        self.db.refresh(uploaded_resume)
        return uploaded_resume

    def get_uploaded_resume_by_uuid(self, resume_uuid: UUID) -> Optional[UploadedResume]:
        """Get uploaded resume by UUID"""
        return self.db.query(UploadedResume).filter(
            UploadedResume.uuid == resume_uuid
        ).first()

    def get_uploaded_resume_by_id(self, resume_id: int) -> Optional[UploadedResume]:
        """Get uploaded resume by ID"""
        return self.db.query(UploadedResume).filter(
            UploadedResume.id == resume_id
        ).first()

    def get_resumes_by_profile(self, profile_id: int) -> List[UploadedResume]:
        """Get all uploaded resumes for a profile"""
        return self.db.query(UploadedResume).filter(
            UploadedResume.profile_id == profile_id
        ).order_by(UploadedResume.created_at.desc()).all()

    def get_resumes_by_user(self, user_id: int) -> List[UploadedResume]:
        """Get all uploaded resumes for a user"""
        return self.db.query(UploadedResume).filter(
            UploadedResume.user_id == user_id
        ).order_by(UploadedResume.created_at.desc()).all()

    def update_resume_status(self, resume: UploadedResume, status: str) -> UploadedResume:
        """Update the import status of a resume"""
        resume.import_status = status
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def update_extracted_data(self, resume: UploadedResume, extracted_data: dict) -> UploadedResume:
        """Update the extracted data for a resume"""
        resume.extracted_data = extracted_data
        self.db.commit()
        self.db.refresh(resume)
        return resume

    def delete_uploaded_resume(self, resume: UploadedResume) -> None:
        """Delete an uploaded resume record"""
        self.db.delete(resume)
        self.db.commit()