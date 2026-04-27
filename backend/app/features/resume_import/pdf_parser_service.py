"""
PDF Parser Service - Extracts structured data from CV PDFs using Docling and LLM
Uses Docling for text extraction, then LLM for structured parsing using actual profile schemas
"""
import logging
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from datetime import date

from features.llm.service import LLMService
from .pdf_extractor import PDFExtractor

# Import actual profile schemas for reference and types
from features.profiles.education.schemas import DegreeType
from features.profiles.skills.schemas import ProficiencyLevel
from features.profiles.languages.schemas import ProficiencyLevel as LangProficiency

logger = logging.getLogger(__name__)


# ============================================================================
# Lenient Schemas for LLM Extraction
# These versions have most fields as Optional to prevent validation failures
# when the LLM cannot find specific required fields (like start_date).
# Validation for database persistence happens in the Service layer.
# ============================================================================

class ContactInfo(BaseModel):
    """Contact information from CV"""
    name: Optional[str] = Field(default=None, description="Full name")
    email: Optional[str] = Field(default=None, description="Email address")
    phone: Optional[str] = Field(default=None, description="Phone number")
    location: Optional[str] = Field(default=None, description="City and state")


class EducationLenient(BaseModel):
    """Lenient education schema for extraction"""
    institution: Optional[str] = Field(None, description="Educational institution name")
    degree: Optional[str] = Field(None, description="Degree or certification name")
    degree_type: Optional[str] = Field(None, description="Type of degree")
    field_of_study: Optional[str] = Field(None, description="Field of study or major")
    start_date: Optional[str] = Field(None, description="Education start date (YYYY-MM-DD or YYYY)")
    end_date: Optional[str] = Field(None, description="Education end date (YYYY-MM-DD or YYYY)")
    gpa: Optional[float] = Field(None, description="GPA or grade")
    description: Optional[str] = Field(None, description="Additional description")


class WorkExperienceLenient(BaseModel):
    """Lenient work experience schema for extraction"""
    job_title: Optional[str] = Field(None, description="Job title")
    company: Optional[str] = Field(None, description="Company name")
    start_date: Optional[str] = Field(None, description="Employment start date (YYYY-MM-DD or YYYY)")
    end_date: Optional[str] = Field(None, description="Employment end date (YYYY-MM-DD or YYYY)")
    description: Optional[str] = Field(None, description="Job description")


class SkillLenient(BaseModel):
    """Lenient skill schema for extraction"""
    name: Optional[str] = Field(None, description="Skill name")
    category: Optional[str] = Field(None, description="Skill category")
    proficiency: Optional[str] = Field(None, description="Proficiency level")
    years_experience: Optional[int] = Field(None, description="Years of experience")


class ProjectLenient(BaseModel):
    """Lenient project schema for extraction"""
    name: Optional[str] = Field(None, description="Project name")
    description: Optional[str] = Field(None, description="Project description")
    start_date: Optional[str] = Field(None, description="Project start date")
    end_date: Optional[str] = Field(None, description="Project end date")
    url: Optional[str] = Field(None, description="Project URL")
    technologies: Optional[str] = Field(None, description="Technologies used")


class CertificateLenient(BaseModel):
    """Lenient certificate schema for extraction"""
    name: Optional[str] = Field(None, description="Certificate name")
    issuing_organization: Optional[str] = Field(None, description="Issuing organization")
    issue_date: Optional[str] = Field(None, description="Issue date")
    expiration_date: Optional[str] = Field(None, description="Expiration date")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    credential_url: Optional[str] = Field(None, description="Credential URL")


class LanguageLenient(BaseModel):
    """Lenient language schema for extraction"""
    language: Optional[str] = Field(None, description="Language name")
    proficiency: Optional[str] = Field(None, description="Proficiency level")


class SummaryLenient(BaseModel):
    """Lenient summary schema for extraction"""
    title: Optional[str] = Field("Professional Summary", description="Summary title")
    content: Optional[str] = Field(None, description="Summary content")


class CustomSectionLenient(BaseModel):
    """Lenient custom section schema for extraction"""
    title: Optional[str] = Field(None, description="Section title")
    content: Optional[str] = Field(None, description="Section content")


class ResumeDataLenient(BaseModel):
    """Complete resume data using lenient schemas for extraction"""
    contact_info: Optional[ContactInfo] = Field(default=None, description="Contact information")
    professional_summaries: Optional[List[SummaryLenient]] = Field(default=None, description="Professional summaries")
    education: Optional[List[EducationLenient]] = Field(default=None, description="Education history")
    work_experiences: Optional[List[WorkExperienceLenient]] = Field(default=None, description="Work experience")
    skills: Optional[List[SkillLenient]] = Field(default=None, description="Skills and competencies")
    projects: Optional[List[ProjectLenient]] = Field(default=None, description="Projects and portfolio items")
    certificates: Optional[List[CertificateLenient]] = Field(default=None, description="Certifications and licenses")
    languages: Optional[List[LanguageLenient]] = Field(default=None, description="Languages spoken")
    custom_sections: Optional[List[CustomSectionLenient]] = Field(default=None, description="Custom sections")


class PDFParserService:
    """Service for parsing PDF CVs using Docling for text extraction and LLM for structured parsing"""

    def __init__(self):
        """Initialize PDF parser with local PDFExtractor and LLMService"""
        self.llm_service = LLMService()
        self.pdf_extractor = PDFExtractor()
        logger.info("PDFParserService initialized with local PDFExtractor and LLMService")

    async def parse_cv_structure(self, file_path: str) -> Dict:
        """
        Extract raw text from PDF using Docling, then use LLM to structure it.
        Uses Groq's tool calling for reliable parsing with lenient schemas.
        """
        try:
            logger.info(f"Extracting text from PDF: {file_path}")
            raw_text = await self.pdf_extractor.extract_text(file_path)

            if not raw_text or len(raw_text.strip()) < 10:
                logger.warning("Extracted text is empty or too short. Resume parsing may fail.")

            logger.info("Parsing resume text with LLM tool calling (Lenient schemas)")
            # Use LLMService's robust function calling method with lenient schema
            resume_data = await self.llm_service.parse_to_model_with_function_calling(
                text=raw_text,
                model_class=ResumeDataLenient,
                instructions=self._get_parsing_instructions(), tool_name="extractresume"
            )

            logger.info("Successfully parsed CV structure with LLM")
            return self._convert_to_dict(resume_data)

        except Exception as e:
            logger.error(f"Error parsing CV structure: {str(e)}", exc_info=True)
            return self._get_empty_resume_data()

    def _get_parsing_instructions(self) -> str:
        """Get detailed instructions for the LLM to parse resume content"""
        return """You are an expert resume parser. Analyze the resume/CV text provided and extract ALL relevant information into the structured format.

EXTRACTION RULES:
1. Contact Information: Extract name, email, phone, location - leave null if not found.
2. Professional Summary: Extract if present (title + content).
3. Education: Extract institution, degree, field of study, dates, GPA, description.
4. Work Experience: Extract job title, company, dates, and description/responsibilities.
5. Skills: Extract skill name, category, proficiency level (Beginner/Intermediate/Advanced/Expert).
6. Projects: Extract name, description, dates, technologies used, URL.
7. Certificates: Extract name, issuing organization, dates, credential ID/URL.
8. Languages: Extract language name and proficiency (Native/Fluent/Conversational/Intermediate/Basic).
9. Custom Sections: Use for ANY content that doesn't fit above categories (Volunteer, Publications, Awards, etc.).

IMPORTANT GUIDELINES:
- Extract EVERYTHING - don't skip any data.
- Use custom_sections as a catch-all for non-standard content.
- Dates: Use "YYYY-MM-DD" format or just "YYYY" if only year is known.
- If optional fields are missing, use null (don't invent data).
- Be thorough - this is capturing the user's complete professional profile."""

    def _convert_to_dict(self, resume_data: ResumeDataLenient) -> Dict:
        """Convert ResumeData model to dictionary with None values removed"""
        data = resume_data.model_dump(exclude_none=True)
        
        # Ensure lists are present even if empty for the service to iterate over them safely
        result = {
            "contact_info": data.get("contact_info", {}),
            "professional_summaries": data.get("professional_summaries", []),
            "education": data.get("education", []),
            "work_experiences": data.get("work_experiences", []),
            "skills": data.get("skills", []),
            "projects": data.get("projects", []),
            "certificates": data.get("certificates", []),
            "languages": data.get("languages", []),
            "custom_sections": data.get("custom_sections", []),
        }
        return result

    def _get_empty_resume_data(self) -> Dict:
        """Return empty resume data structure"""
        return {
            "contact_info": {},
            "professional_summaries": [],
            "education": [],
            "work_experiences": [],
            "skills": [],
            "projects": [],
            "certificates": [],
            "languages": [],
            "custom_sections": [],
        }