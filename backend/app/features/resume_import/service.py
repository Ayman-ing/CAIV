"""
Resume Import Service - Business logic for resume upload and processing
"""
import logging
from typing import Dict, Any, Optional
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session

from core.exceptions import HTTPException
from features.profiles.models import Profile
from features.users.models import User
from features.profiles.education.repository import EducationRepository
from features.profiles.education.schemas import EducationCreate
from features.profiles.work_experiences.repository import WorkExperienceRepository
from features.profiles.work_experiences.schemas import WorkExperienceCreate
from features.profiles.skills.repository import SkillRepository
from features.profiles.skills.schemas import SkillCreate
from features.profiles.certificates.repository import CertificateRepository
from features.profiles.certificates.schemas import CertificateCreate
from features.profiles.languages.repository import LanguageRepository
from features.profiles.languages.schemas import LanguageCreate
from features.profiles.projects.repository import ProjectRepository
from features.profiles.professional_summaries.repository import ProfessionalSummaryRepository
from features.profiles.professional_summaries.schemas import ProfessionalSummaryCreate
from features.profiles.projects.schemas import ProjectCreate
from features.profiles.custom_sections.repository import CustomSectionRepository
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
        
        # Initialize sub-repositories
        self.education_repo = EducationRepository(db)
        self.work_exp_repo = WorkExperienceRepository(db)
        self.skills_repo = SkillRepository(db)
        self.certificates_repo = CertificateRepository(db)
        self.languages_repo = LanguageRepository(db)
        self.projects_repo = ProjectRepository(db)
        self.professional_summary_repo = ProfessionalSummaryRepository(db)
        self.custom_sections_repo = CustomSectionRepository(db)

    async def upload_and_parse_resume(
        self,
        profile_id: UUID,
        user_id: int,
        file_path: str,
        filename: str
    ) -> ResumeUploadResponse:
        """
        Upload a resume file, parse it with Docling, and return extracted data
        """
        try:
            # Get profile to verify it exists and belongs to user
            profile = self._get_profile_by_uuid(profile_id)
            if not profile:
                raise HTTPException(status_code=404, message="Profile not found")

            if profile.user_id != user_id:
                raise HTTPException(status_code=403, message="Profile does not belong to user")

            # Parse structured data from PDF
            logger.info(f"Parsing structured data from PDF: {filename}")
            extracted_data = await self.pdf_parser.parse_cv_structure(file_path)

            # Store in database
            uploaded_resume = self.repo.create_uploaded_resume(
                profile_id=profile.id,
                user_id=user_id,
                filename=filename,
                extracted_data=extracted_data
            )

            # NOTE: We no longer populate the profile immediately.
            # The user must call the /confirm endpoint to apply changes.
            logger.info(f"Successfully uploaded and parsed resume: {uploaded_resume.uuid}")

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
            logger.error(f"Error uploading and parsing resume: {e}")
            raise HTTPException(
                status_code=500,
                message=f"Failed to process resume: {str(e)}"
            )

    def confirm_resume_import(self, resume_id: UUID, user_id: int, confirm: bool) -> ResumeImportStatus:
        """Confirm or reject a resume import"""
        uploaded_resume = self.repo.get_uploaded_resume_by_uuid(resume_id)
        if not uploaded_resume:
            raise HTTPException(status_code=404, message="Resume not found")

        if uploaded_resume.user_id != user_id:
            raise HTTPException(status_code=403, message="Access denied")

        # Update status
        if confirm and uploaded_resume.import_status == "pending":
            # Populate profile now that user confirmed
            logger.info(f"User confirmed resume import {resume_id}. Populating profile...")
            profile = uploaded_resume.profile
            self._populate_profile_from_extracted_data(profile, uploaded_resume.extracted_data)
            new_status = "confirmed"
        elif confirm:
            new_status = "confirmed"
        else:
            new_status = "rejected"

        updated_resume = self.repo.update_resume_status(uploaded_resume, new_status)
        logger.info(f"Resume {resume_id} status updated to: {new_status}")

        return ResumeImportStatus(
            resume_id=updated_resume.uuid,
            status=updated_resume.import_status,
            extracted_data=updated_resume.extracted_data,
            updated_at=updated_resume.updated_at
        )

    def _populate_profile_from_extracted_data(self, profile: Profile, extracted_data: Dict[str, Any]) -> None:
        """Populate profile and its sections with extracted data"""
        try:
            logger.info(f"Populating profile {profile.id} with extracted sections")

            # Update profile contact information
            self._update_profile_contact_info(profile, extracted_data.get("contact_info", {}))
            
            # Sections to process
            sections = [
                ("education", self._create_education_from_extracted),
                ("work_experiences", self._create_work_experience_from_extracted),
                ("skills", self._create_skill_from_extracted),
                ("certificates", self._create_certificate_from_extracted),
                ("languages", self._create_language_from_extracted),
                ("projects", self._create_project_from_extracted),
                ("professional_summaries", self._create_professional_summary_from_extracted),
                ("custom_sections", self._create_custom_section_from_extracted),
            ]

            for key, creator_fn in sections:
                entries = extracted_data.get(key, [])
                if not isinstance(entries, list):
                    continue
                for entry in entries:
                    try:
                        creator_fn(profile.id, entry)
                    except Exception as e:
                        logger.warning(f"Failed to create entry in {key}: {e}")
                        self.db.rollback() # Clear failed transaction state so next items can proceed
            
        except Exception as e:
            logger.error(f"Error populating profile from extracted data: {e}")
            raise

    def _update_profile_contact_info(self, profile: Profile, contact_info: Dict[str, Any]) -> None:
        """Update profile with contact information"""
        if not contact_info: return
        
        modified = False
        if contact_info.get("name") and not profile.name:
            profile.name = contact_info["name"]
            modified = True
        if contact_info.get("email") and not profile.email:
            profile.email = contact_info["email"]
            modified = True
        if contact_info.get("phone") and not profile.phone_number:
            profile.phone_number = contact_info["phone"]
            modified = True
        if contact_info.get("location") and not profile.location:
            profile.location = contact_info["location"]
            modified = True
        
        if modified:
            self.db.commit()
            logger.info(f"Updated profile {profile.id} contact information")

    def _create_education_from_extracted(self, profile_id: int, edu_data: Dict[str, Any]) -> None:
        if not edu_data.get("institution") or not edu_data.get("degree"):
            return
        
        # Ensure we have a start_date, otherwise provide a safe default
        start_date = self._parse_date(edu_data.get("start_date")) or date(2000, 1, 1)

        degree_type = self._map_degree_type(edu_data.get("degree_type"))
        
        education_create = EducationCreate(
            institution=edu_data["institution"],
            degree=edu_data["degree"],
            degree_type=degree_type,
            field_of_study=edu_data.get("field_of_study"),
            start_date=start_date,
            end_date=self._parse_date(edu_data.get("end_date")),
            gpa=self._parse_float(edu_data.get("gpa")),
            description=edu_data.get("description")
        )
        self.education_repo.create_with_profile_id(profile_id, education_create)

    def _create_work_experience_from_extracted(self, profile_id: int, exp_data: Dict[str, Any]) -> None:
        if not exp_data.get("job_title") or not exp_data.get("company"):
            return
        
        start_date = self._parse_date(exp_data.get("start_date")) or date(2000, 1, 1)
        
        work_exp_create = WorkExperienceCreate(
            job_title=exp_data["job_title"],
            company=exp_data["company"],
            start_date=start_date,
            end_date=self._parse_date(exp_data.get("end_date")),
            description=exp_data.get("description")
        )
        self.work_exp_repo.create_with_profile_id(profile_id, work_exp_create)

    def _create_skill_from_extracted(self, profile_id: int, skill_data: Dict[str, Any]) -> None:
        if not skill_data.get("name"):
            return
        
        proficiency = self._map_skill_proficiency(skill_data.get("proficiency"))
        
        skill_create = SkillCreate(
            name=skill_data["name"],
            category=skill_data.get("category") or "Technical",
            proficiency=proficiency,
            years_experience=self._parse_int(skill_data.get("years_experience"))
        )
        self.skills_repo.create_with_profile_id(profile_id, skill_create)

    def _create_certificate_from_extracted(self, profile_id: int, cert_data: Dict[str, Any]) -> None:
        if not cert_data.get("name"):
            return
        
        cert_create = CertificateCreate(
            name=cert_data["name"],
            issuing_organization=cert_data.get("issuing_organization") or "Unknown",
            issue_date=self._parse_date(cert_data.get("issue_date")) or date(2020, 1, 1),
            expiration_date=self._parse_date(cert_data.get("expiration_date")),
            credential_id=cert_data.get("credential_id"),
            credential_url=cert_data.get("credential_url")
        )
        
        # Convert HttpUrl to string if present, as psycopg2 doesn't adapt it automatically
        if cert_create.credential_url:
            cert_create.credential_url = str(cert_create.credential_url) # type: ignore
            
        self.certificates_repo.create_with_profile_id(profile_id, cert_create)

    def _create_language_from_extracted(self, profile_id: int, lang_data: Dict[str, Any]) -> None:
        if not lang_data.get("language"):
            return
        
        proficiency = self._map_proficiency_level(lang_data.get("proficiency", "Intermediate"))
        
        lang_create = LanguageCreate(
            language=lang_data["language"],
            proficiency=proficiency,
            can_read=lang_data.get("can_read", True),
            can_write=lang_data.get("can_write", True),
            can_speak=lang_data.get("can_speak", True)
        )
        self.languages_repo.create_with_profile_id(profile_id, lang_create)

    def _create_project_from_extracted(self, profile_id: int, proj_data: Dict[str, Any]) -> None:
        if not proj_data.get("name"):
            return
        
        proj_create = ProjectCreate(
            name=proj_data["name"],
            description=proj_data.get("description"),
            start_date=self._parse_date(proj_data.get("start_date")) or date(2020, 1, 1),
            end_date=self._parse_date(proj_data.get("end_date")),
            url=proj_data.get("url"),
            technologies=proj_data.get("technologies")
        )
        
        # Convert HttpUrl to string if present
        if proj_create.url:
            proj_create.url = str(proj_create.url) # type: ignore
            
        self.projects_repo.create_with_profile_id(profile_id, proj_create)

    def _create_professional_summary_from_extracted(self, profile_id: int, summary_data: Dict[str, Any]) -> None:
        if not summary_data.get("content") or not summary_data["content"].strip():
            return
        
        summary_create = ProfessionalSummaryCreate(
            title=summary_data.get("title") or "Professional Summary",
            content=summary_data["content"][:1000]
        )
        self.professional_summary_repo.create(profile_id, summary_create)

    def _create_custom_section_from_extracted(self, profile_id: int, custom_data: Dict[str, Any]) -> None:
        if not custom_data.get("title") or not custom_data.get("content"):
            return

        custom_create = CustomSectionCreate(
            title=custom_data["title"],
            content=custom_data["content"],
            order_index=custom_data.get("order_index", 0)
        )
        self.custom_sections_repo.create(profile_id, custom_create)

    def _parse_date(self, date_value: Any) -> Optional[date]:
        if not date_value: return None
        if isinstance(date_value, date): return date_value
        if isinstance(date_value, str):
            from datetime import datetime
            date_str = date_value.strip()
            if len(date_str) == 4 and date_str.isdigit():
                return date(int(date_str), 1, 1)
            for fmt in ('%B %Y', '%m/%Y', '%Y-%m-%d', '%d/%m/%Y'):
                try:
                    return datetime.strptime(date_str, fmt).date()
                except ValueError: continue
        return None

    def _parse_float(self, value: Any) -> Optional[float]:
        try: return float(value) if value is not None else None
        except (ValueError, TypeError): return None

    def _parse_int(self, value: Any) -> Optional[int]:
        try: return int(float(value)) if value is not None else None
        except (ValueError, TypeError): return None

    def _map_proficiency_level(self, proficiency: Optional[str]) -> str:
        if not proficiency: return "Intermediate"
        p = proficiency.lower()
        if "native" in p or "bilingual" in p: return "Native"
        if "fluent" in p or "proficient" in p: return "Fluent"
        if "conversational" in p or "working" in p: return "Conversational"
        if "intermediate" in p: return "Intermediate"
        if "basic" in p or "elementary" in p: return "Basic"
        return "Intermediate"

    def _map_skill_proficiency(self, proficiency: Optional[str]) -> str:
        if not proficiency: return "Intermediate"
        p = proficiency.lower()
        if "expert" in p or "master" in p or "lead" in p: return "Expert"
        if "advanced" in p or "senior" in p or "proficient" in p: return "Advanced"
        if "intermediate" in p or "medium" in p or "middle" in p: return "Intermediate"
        if "beginner" in p or "junior" in p or "basic" in p or "entry" in p: return "Beginner"
        return "Intermediate"

    def _map_degree_type(self, degree_type: Optional[str]) -> str:
        if not degree_type: return "Other"
        d = degree_type.lower()
        if "bachelor" in d or "licence" in d or "engineering degree" in d: return "Bachelor"
        if "master" in d or "magistère" in d or "msc" in d: return "Master"
        if "phd" in d or "doctorate" in d: return "PhD"
        if "associate" in d: return "Associate"
        if "high school" in d or "baccalaureate" in d or "bac" in d: return "High School Diploma"
        if "professional" in d: return "Professional"
        if "certificate" in d or "certification" in d: return "Certificate"
        return "Other"

    def get_resume_status(self, resume_id: UUID, user_id: int) -> ResumeImportStatus:
        uploaded_resume = self.repo.get_uploaded_resume_by_uuid(resume_id)
        if not uploaded_resume or uploaded_resume.user_id != user_id:
            raise HTTPException(status_code=404, message="Resume not found")
        return ResumeImportStatus(
            resume_id=uploaded_resume.uuid,
            status=uploaded_resume.import_status,
            extracted_data=uploaded_resume.extracted_data,
            updated_at=uploaded_resume.updated_at
        )

    def get_user_resumes(self, user_id: int) -> Dict[str, Any]:
        resumes = self.repo.get_resumes_by_user(user_id)
        return {"resumes": [{
            "resume_id": str(r.uuid),
            "filename": r.original_filename,
            "status": r.import_status,
            "created_at": r.created_at.isoformat()
        } for r in resumes]}

    def _get_profile_by_uuid(self, profile_uuid: UUID) -> Optional[Profile]:
        return self.db.query(Profile).filter(Profile.uuid == profile_uuid).first()
