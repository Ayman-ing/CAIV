"""
Resume Import Service - Business logic for resume upload and processing.
Refactored to be cleaner, using feature services instead of direct repository access.
"""
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from core.exceptions import HTTPException
from features.profiles.repository import ProfileRepository

# Import Feature Services
from features.profiles.education.service import EducationService
from features.profiles.education.schemas import EducationCreate
from features.profiles.work_experiences.service import WorkExperienceService
from features.profiles.work_experiences.schemas import WorkExperienceCreate
from features.profiles.skills.service import SkillService
from features.profiles.skills.schemas import SkillCreate
from features.profiles.certificates.service import CertificateService
from features.profiles.certificates.schemas import CertificateCreate
from features.profiles.languages.service import LanguageService
from features.profiles.languages.schemas import LanguageCreate
from features.profiles.projects.service import ProjectService
from features.profiles.projects.schemas import ProjectCreate
from features.profiles.professional_summaries.service import ProfessionalSummaryService
from features.profiles.professional_summaries.schemas import ProfessionalSummaryCreate
from features.profiles.custom_sections.service import CustomSectionService
from features.profiles.custom_sections.schemas import CustomSectionCreate

from .repository import ResumeImportRepository
from .pdf_parser_service import PDFParserService
from .schemas import ResumeUploadResponse, ResumeImportStatus


logger = logging.getLogger(__name__)


class ResumeImportService:
    """Service for handling resume import operations"""

    def __init__(self, db: Session):
        self.db = db
        self.repo = ResumeImportRepository(db)
        self.pdf_parser = PDFParserService()
        self.profile_repo = ProfileRepository(db)
        
        # Initialize Feature Services
        self.education_service = EducationService(db)
        self.work_exp_service = WorkExperienceService(db)
        self.skills_service = SkillService(db)
        self.certificates_service = CertificateService(db)
        self.languages_service = LanguageService(db)
        self.projects_service = ProjectService(db)
        self.summary_service = ProfessionalSummaryService(db)
        self.custom_sections_service = CustomSectionService(db)

    async def upload_and_parse_resume(
        self,
        profile_id: UUID,
        user_id: int,
        file_path: str,
        filename: str
    ) -> ResumeUploadResponse:
        """Upload a resume file, parse it, and return extracted data"""
        try:
            # Verify profile ownership
            profile = self.profile_repo.get_by_uuid(str(profile_id))
            if not profile or profile.user_id != user_id:
                raise HTTPException(status_code=403, message="Access denied to this profile")

            # Parse structured data from PDF
            logger.info(f"Starting PDF parsing for: {filename}")
            extracted_data = await self.pdf_parser.parse_cv_structure(file_path)

            # Store extraction result for user confirmation
            uploaded_resume = self.repo.create_uploaded_resume(
                profile_id=profile.id,
                user_id=user_id,
                filename=filename,
                extracted_data=extracted_data
            )

            return ResumeUploadResponse(
                resume_id=uploaded_resume.uuid,
                filename=uploaded_resume.original_filename,
                status=uploaded_resume.import_status,
                extracted_data=uploaded_resume.extracted_data,
                created_at=uploaded_resume.created_at
            )

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing resume: {e}")
            raise HTTPException(status_code=500, message=f"Failed to process resume: {str(e)}")

    def confirm_resume_import(self, resume_id: UUID, user_id: int, confirm: bool) -> ResumeImportStatus:
        """Confirm or reject a resume import"""
        uploaded_resume = self.repo.get_uploaded_resume_by_uuid(resume_id)
        if not uploaded_resume or uploaded_resume.user_id != user_id:
            raise HTTPException(status_code=404, message="Resume record not found")

        if confirm and uploaded_resume.import_status == "pending":
            logger.info(f"Importing data from resume {resume_id} into profile {uploaded_resume.profile.uuid}")
            self._populate_profile(str(uploaded_resume.profile.uuid), uploaded_resume.extracted_data)
            status = "confirmed"
        else:
            status = "confirmed" if confirm else "rejected"

        updated = self.repo.update_resume_status(uploaded_resume, status)
        return ResumeImportStatus(
            resume_id=updated.uuid,
            status=updated.import_status,
            extracted_data=updated.extracted_data,
            updated_at=updated.updated_at
        )

    def _populate_profile(self, profile_uuid: str, data: Dict[str, Any]) -> None:
        """Populate profile sections using feature services"""
        
        # Mapping of data keys to their respective services and schemas
        sections = [
            ("education", self.education_service.create_education, EducationCreate),
            ("work_experiences", self.work_exp_service.create_work_experience, WorkExperienceCreate),
            ("skills", self.skills_service.create_skill, SkillCreate),
            ("certificates", self.certificates_service.create_certificate, CertificateCreate),
            ("languages", self.languages_service.create_language, LanguageCreate),
            ("projects", self.projects_service.create_project, ProjectCreate),
            ("professional_summaries", self.summary_service.create, ProfessionalSummaryCreate),
            ("custom_sections", self.custom_sections_service.create_custom_section, CustomSectionCreate),
        ]

        # Update core profile info if available
        contact = data.get("contact_info", {})
        if contact:
            from features.profiles.schemas import ProfileUpdate
            db_profile = self.profile_repo.get_by_uuid(profile_uuid)
            if db_profile:
                update_data = ProfileUpdate(
                    name=contact.get("name"),
                    email=contact.get("email"),
                    phone_number=contact.get("phone"),
                    location=contact.get("location")
                )
                self.profile_repo.update(db_profile, update_data)

        # Import each section
        for key, create_method, schema_class in sections:
            items = data.get(key, [])
            if not isinstance(items, list): continue
            
            for item in items:
                try:
                    # Validate and convert raw dict to Pydantic model
                    # This handles date string -> date object conversion automatically
                    validated_item = schema_class.model_validate(item)
                    create_method(profile_uuid, validated_item)
                except Exception as e:
                    # Log detailed field-level errors for Pydantic ValidationErrors
                    try:
                        from pydantic import ValidationError
                        if isinstance(e, ValidationError):
                            for err in e.errors():
                                logger.warning(
                                    f"  → {key} field '{'.'.join(str(l) for l in err['loc'])}': "
                                    f"{err['msg']} (type={err['type']}, input={err.get('input')})"
                                )
                    except Exception:
                        pass
                    logger.warning(f"Skipping {key} item due to validation error: {e}")
                    self.db.rollback()  # Reset transaction after failed item
                    
                    # Do not fall back if the item is already a custom section
                    if key == "custom_sections":
                        continue
                        
                    # ULTIMATE FAILSAFE: Convert failed item to a Custom Section to avoid data loss
                    try:
                        details = []
                        for k, v in item.items():
                            if v is not None:
                                label = k.replace("_", " ").title()
                                details.append(f"**{label}**: {v}")
                        
                        title = f"Unresolved {key.replace('_', ' ').title()} (Imported)"
                        content = "\n".join(details)
                        
                        custom_schema = CustomSectionCreate(title=title, content=content)
                        self.custom_sections_service.create_custom_section(profile_uuid, custom_schema)
                        logger.info(f"Gracefully recovered failed {key} item into custom sections")
                    except Exception as fallback_err:
                        logger.error(f"Failed to save fallback custom section: {fallback_err}")
                        self.db.rollback()

    def get_resume_status(self, resume_id: UUID, user_id: int) -> ResumeImportStatus:
        res = self.repo.get_uploaded_resume_by_uuid(resume_id)
        if not res or res.user_id != user_id:
            raise HTTPException(status_code=404, message="Resume not found")
        return ResumeImportStatus(
            resume_id=res.uuid,
            status=res.import_status,
            extracted_data=res.extracted_data,
            updated_at=res.updated_at
        )

    def get_user_resumes(self, user_id: int) -> Dict[str, Any]:
        resumes = self.repo.get_resumes_by_user(user_id)
        return {"resumes": [
            {
                "resume_id": str(r.uuid),
                "filename": r.original_filename,
                "status": r.import_status,
                "created_at": r.created_at.isoformat()
            } for r in resumes
        ]}
