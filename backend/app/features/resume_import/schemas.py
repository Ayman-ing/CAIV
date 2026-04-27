"""
Resume Import Schemas - Pydantic models for API requests/responses
"""
from pydantic import BaseModel, Field, UUID4
from typing import Optional, Dict, List, Any
from datetime import datetime
from uuid import UUID


class ResumeUploadRequest(BaseModel):
    """Schema for resume upload request"""

    profile_id: UUID4 = Field(..., description="UUID of the profile to associate the resume with")

    model_config = {
        "json_schema_extra": {
            "example": {
                "profile_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }


class ResumeUploadResponse(BaseModel):
    """Schema for resume upload response"""

    resume_id: UUID4 = Field(..., description="UUID of the uploaded resume")
    filename: str = Field(..., description="Original filename of uploaded resume")
    status: str = Field(..., description="Import status (pending, confirmed, rejected)")
    extracted_data: Optional[Dict[str, Any]] = Field(None, description="Extracted data from the resume")
    created_at: datetime = Field(..., description="Upload timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_id": "123e4567-e89b-12d3-a456-426614174001",
                "filename": "john_doe_resume.pdf",
                "status": "pending",
                "extracted_data": {
                    "contact_info": {"name": "John Doe", "email": "john@example.com"},
                    "education": [{"institution": "MIT", "degree": "Bachelor of Science"}],
                    "work_experience": [{"job_title": "Software Engineer", "company": "Google"}]
                },
                "created_at": "2024-01-15T10:30:00Z"
            }
        }
    }


class ResumeImportStatus(BaseModel):
    """Schema for resume import status"""

    resume_id: UUID4 = Field(..., description="UUID of the resume")
    status: str = Field(..., description="Current import status")
    extracted_data: Optional[Dict[str, Any]] = Field(None, description="Extracted data if available")
    updated_at: datetime = Field(..., description="Last update timestamp")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_id": "123e4567-e89b-12d3-a456-426614174001",
                "status": "confirmed",
                "extracted_data": {
                    "contact_info": {"name": "John Doe", "email": "john@example.com"}
                },
                "updated_at": "2024-01-15T10:35:00Z"
            }
        }
    }


class ResumeConfirmImport(BaseModel):
    """Schema for confirming resume import"""

    resume_id: UUID4 = Field(..., description="UUID of the resume to confirm")
    confirm: bool = Field(..., description="Whether to confirm (true) or reject (false) the import")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resume_id": "123e4567-e89b-12d3-a456-426614174001",
                "confirm": True
            }
        }
    }


class ResumeListResponse(BaseModel):
    """Schema for listing uploaded resumes"""

    resumes: List[Dict[str, Any]] = Field(..., description="List of uploaded resumes")

    model_config = {
        "json_schema_extra": {
            "example": {
                "resumes": [
                    {
                        "resume_id": "123e4567-e89b-12d3-a456-426614174001",
                        "filename": "resume.pdf",
                        "status": "confirmed",
                        "created_at": "2024-01-15T10:30:00Z"
                    }
                ]
            }
        }
    }