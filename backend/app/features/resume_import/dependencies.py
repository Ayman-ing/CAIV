"""
Resume Import Dependencies - FastAPI dependency injection
"""
from fastapi import Depends, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from uuid import UUID

from db.session import get_db
from features.users.models import User
from features.auth.dependencies import get_current_user
from .service import ResumeImportService


def get_resume_import_service(db: Session = Depends(get_db)) -> ResumeImportService:
    """Dependency to get ResumeImportService instance"""
    return ResumeImportService(db)


async def validate_resume_upload(
    profile_id: str = Form(...),
    resume: UploadFile = File(...)  # must match FormData field name sent by frontend
) -> dict:
    """
    Validate resume upload request

    Args:
        profile_id: Profile UUID as string
        resume: Uploaded file

    Returns:
        Dictionary with validated data
    """
    # Validate profile_id is a valid UUID
    try:
        profile_uuid = UUID(profile_id)
    except ValueError:
        from core.exceptions import HTTPException
        raise HTTPException(
            status_code=400,
            message="Invalid profile_id format"
        )

    # Validate file type
    if not resume.filename.lower().endswith('.pdf'):
        from core.exceptions import HTTPException
        raise HTTPException(
            status_code=400,
            message="Only PDF files are supported"
        )

    # Validate file size (max 10MB)
    max_size = 10 * 1024 * 1024  # 10MB
    file_content = await resume.read()
    if len(file_content) > max_size:
        from core.exceptions import HTTPException
        raise HTTPException(
            status_code=400,
            message="File size exceeds 10MB limit"
        )

    return {
        "profile_id": profile_uuid,
        "file_content": file_content,
        "filename": resume.filename
    }