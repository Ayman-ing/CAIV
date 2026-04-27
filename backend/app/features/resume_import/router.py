"""
Resume Import Router - API endpoints for resume upload and processing
"""
import tempfile
import os
from fastapi import APIRouter, Depends, UploadFile, File, Form, status
from typing import Dict, Any
from uuid import UUID

from features.users.models import User
from features.auth.dependencies import get_current_user
from .service import ResumeImportService
from .dependencies import get_resume_import_service, validate_resume_upload
from .schemas import (
    ResumeUploadResponse,
    ResumeImportStatus,
    ResumeConfirmImport,
    ResumeListResponse
)


router = APIRouter(prefix="/api/v1/resume-import", tags=["resume-import"])


@router.post("/upload", response_model=ResumeUploadResponse, status_code=status.HTTP_201_CREATED)
async def upload_resume(
    validated_data: dict = Depends(validate_resume_upload),
    current_user: User = Depends(get_current_user),
    resume_import_service: ResumeImportService = Depends(get_resume_import_service)
):
    """
    Upload and parse a resume PDF

    The resume will be processed using Docling to extract structured data
    including contact info, education, work experience, skills, etc.
    """
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as temp_file:
        temp_file.write(validated_data["file_content"])
        temp_file_path = temp_file.name

    try:
        # Process the resume
        result = await resume_import_service.upload_and_parse_resume(
            profile_id=validated_data["profile_id"],
            user_id=current_user.id,
            file_path=temp_file_path,
            filename=validated_data["filename"]
        )

        return result

    finally:
        # Clean up temporary file
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


@router.get("/status/{resume_id}", response_model=ResumeImportStatus)
async def get_resume_status(
    resume_id: UUID,
    current_user: User = Depends(get_current_user),
    resume_import_service: ResumeImportService = Depends(get_resume_import_service)
):
    """
    Get the processing status and extracted data for an uploaded resume
    """
    return resume_import_service.get_resume_status(resume_id, current_user.id)


@router.post("/confirm", response_model=ResumeImportStatus)
async def confirm_resume_import(
    confirm_data: ResumeConfirmImport,
    current_user: User = Depends(get_current_user),
    resume_import_service: ResumeImportService = Depends(get_resume_import_service)
):
    """
    Confirm or reject a resume import

    When confirmed, the extracted data can be used to populate the user's profile.
    When rejected, the resume data is marked as not usable.
    """
    return resume_import_service.confirm_resume_import(
        confirm_data.resume_id,
        current_user.id,
        confirm_data.confirm
    )


@router.get("/list", response_model=ResumeListResponse)
async def list_user_resumes(
    current_user: User = Depends(get_current_user),
    resume_import_service: ResumeImportService = Depends(get_resume_import_service)
):
    """
    List all resumes uploaded by the current user
    """
    return resume_import_service.get_user_resumes(current_user.id)