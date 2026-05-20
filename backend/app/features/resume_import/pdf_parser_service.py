"""
PDF Parser Service - Extracts structured data from CV PDFs using Docling and LLM.
Consolidated to handle both text extraction and structured parsing.
"""

import logging
import asyncio
from typing import Dict, List, Optional, Any, Union, get_args
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from pathlib import Path

# Docling imports
from docling.datamodel.base_models import InputFormat
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions, AcceleratorOptions

from features.llm.service import LLMService

# Import actual profile schemas for valid enum values
from features.profiles.education.schemas import DegreeType
from features.profiles.skills.schemas import ProficiencyLevel
from features.profiles.languages.schemas import ProficiencyLevel as LangProficiency

logger = logging.getLogger(__name__)

# ============================================================================
# Smarter Extraction Schemas
# These models nudge the LLM toward correct types and provide fallback defaults.
# ============================================================================


class ContactInfo(BaseModel):
    name: Optional[str] = Field(None, description="Full name")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")
    location: Optional[str] = Field(None, description="City and state/country")


class EducationLenient(BaseModel):
    institution: str = Field(
        default="Unknown Institution", description="Educational institution name"
    )
    degree: str = Field(
        default="Unknown Degree", description="Degree or certification name"
    )
    degree_type: Union[DegreeType, str, None] = Field(
        default="Other", description="Category of degree"
    )
    field_of_study: Optional[str] = Field(None, description="Field of study")
    start_date: Union[date, str, None] = Field(
        default="1900-01-01", description="Start date (YYYY-MM-DD)"
    )
    end_date: Union[date, str, None] = Field(None, description="End date (YYYY-MM-DD)")
    gpa: Optional[float] = Field(None, description="GPA/Grade")
    description: Optional[str] = Field(None, description="Additional details")

    @field_validator("degree_type", mode="before")
    @classmethod
    def validate_degree_type(cls, v: Any) -> Any:
        valid_values = get_args(DegreeType) or (
            "High School Diploma",
            "Associate",
            "Bachelor",
            "Master",
            "PhD",
            "Professional",
            "Certificate",
            "Other",
        )
        if not v or v not in valid_values:
            return "Other"
        return v


class WorkExperienceLenient(BaseModel):
    job_title: str = Field(default="Unknown Position", description="Job title")
    company: str = Field(default="Unknown Company", description="Company name")
    start_date: Union[date, str, None] = Field(
        default="1900-01-01", description="Start date (YYYY-MM-DD)"
    )
    end_date: Union[date, str, None] = Field(None, description="End date (YYYY-MM-DD)")
    description: Optional[str] = Field(
        None,
        description="Detailed job description. Include ALL bullet points, responsibilities, and achievements. Do not summarize.",
    )


class SkillLenient(BaseModel):
    name: str = Field(..., description="Skill name")
    category: str = Field(
        default="Other",
        description="Skill category. Choose the closest from: Programming Languages, Frameworks & Libraries, Databases, Cloud & DevOps, Tools & Software, Operating Systems, Soft Skills, Languages, Other.",
    )
    proficiency: Union[ProficiencyLevel, str, None] = Field(
        default="Intermediate", description="Proficiency level"
    )
    years_experience: Optional[int] = Field(None, description="Years of experience")

    @field_validator("proficiency", mode="before")
    @classmethod
    def validate_proficiency(cls, v: Any) -> Any:
        valid_values = get_args(ProficiencyLevel) or (
            "Beginner",
            "Intermediate",
            "Advanced",
            "Expert",
        )
        if not v or v not in valid_values:
            return "Intermediate"
        return v


class ProjectLenient(BaseModel):
    name: str = Field(default="Unknown Project", description="Project name")
    description: Optional[str] = Field(
        None,
        description="Detailed project description. Include ALL features, technologies used, and your specific contributions.",
    )
    start_date: Union[date, str, None] = Field(None, description="Start date")
    end_date: Union[date, str, None] = Field(None, description="End date")
    url: Optional[str] = Field(None, description="Project URL")
    technologies: Optional[str] = Field(
        None, description="Technologies used (comma separated)"
    )


class CertificateLenient(BaseModel):
    name: str = Field(default="Unknown Certificate", description="Certificate name")
    issuing_organization: str = Field(
        default="Unknown Issuer", description="Issuing organization"
    )
    issue_date: Union[date, str, None] = Field(None, description="Issue date")
    expiration_date: Union[date, str, None] = Field(None, description="Expiration date")
    credential_id: Optional[str] = Field(None, description="Credential ID")
    credential_url: Optional[str] = Field(None, description="Credential URL")


class LanguageLenient(BaseModel):
    language: str = Field(..., description="Language name")
    proficiency: Union[LangProficiency, str, None] = Field(
        default=LangProficiency.INTERMEDIATE, description="Proficiency level"
    )

    @field_validator("proficiency", mode="before")
    @classmethod
    def validate_proficiency(cls, v: Any) -> Any:
        valid_values = [e.value for e in LangProficiency]
        if not v or v not in valid_values:
            return LangProficiency.INTERMEDIATE
        return v


class SummaryLenient(BaseModel):
    title: str = Field(default="Professional Summary", description="Summary title")
    content: str = Field(..., description="Summary content")


class CustomSectionLenient(BaseModel):
    title: str = Field(..., description="Section title")
    content: str = Field(..., description="Section content")



def normalize_date_str(val: Any) -> Optional[str]:
    if not val:
        return None
    if isinstance(val, (date, datetime)):
        return val.strftime("%Y-%m-%d")
        
    val_str = str(val).strip()
    if not val_str:
        return None
        
    # Standardize common "present" indicators
    if val_str.lower() in ("present", "current", "ongoing", "now", "active", "en cours", "today"):
        return None
        
    import re
    
    # Try exact YYYY-MM-DD
    match = re.search(r"\b(19\d{2}|20\d{2})-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01])\b", val_str)
    if match:
        return f"{match.group(1)}-{match.group(2)}-{match.group(3)}"
        
    # Try Month/Year patterns: MM/YYYY, M/YYYY, MM-YYYY, MM.YYYY
    match = re.search(r"\b(0?[1-9]|1[0-2])[-/.\s]+(19\d{2}|20\d{2})\b", val_str)
    if match:
        month = int(match.group(1))
        year = match.group(2)
        return f"{year}-{month:02d}-01"
        
    # Try Year/Month patterns: YYYY/MM, YYYY-MM, YYYY.MM
    match = re.search(r"\b(19\d{2}|20\d{2})[-/.\s]+(0?[1-9]|1[0-2])\b", val_str)
    if match:
        year = match.group(1)
        month = int(match.group(2))
        return f"{year}-{month:02d}-01"
        
    # Try textual month names
    months_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
        "janvier": 1, "fevrier": 2, "février": 2, "mars": 3, "avril": 4,
        "mai": 5, "juin": 6, "juillet": 7, "aout": 8, "août": 8,
        "septembre": 9, "octobre": 10, "novembre": 11, "decembre": 12, "décembre": 12
    }
    
    val_lower = val_str.lower()
    for name, num in months_map.items():
        if name in val_lower:
            year_match = re.search(r"\b(19\d{2}|20\d{2})\b", val_str)
            if year_match:
                return f"{year_match.group(1)}-{num:02d}-01"
                
    # Fallback to year-only if a 4-digit number is found
    year_match = re.search(r"\b(19\d{2}|20\d{2})\b", val_str)
    if year_match:
        return f"{year_match.group(1)}-01-01"
        
    return None


def clean_url_str(val: Any) -> Optional[str]:
    if not val:
        return None
    val_str = str(val).strip()
    if not val_str:
        return None
    if val_str.startswith(("http://", "https://")):
        return val_str
    if "." in val_str or val_str.startswith("www"):
        return f"https://{val_str}"
    return val_str


def clean_gpa(val: Any) -> Optional[float]:
    if val is None:
        return None
    if isinstance(val, (int, float)):
        gpa = float(val)
    else:
        val_str = str(val).strip()
        # Try parsing a fraction like 15/20 -> 15.0
        import re
        match = re.match(r"^(\d+(?:\.\d+)?)\s*/\s*\d+$", val_str)
        if match:
            val_str = match.group(1)
        try:
            gpa = float(val_str)
        except ValueError:
            return None
    if 0.0 <= gpa <= 20.0:
        return gpa
    return None


class ResumeDataLenient(BaseModel):
    """The master schema sent to the LLM via tool calling"""

    contact_info: Optional[ContactInfo] = None
    professional_summaries: List[SummaryLenient] = Field(default_factory=list)
    education: List[EducationLenient] = Field(default_factory=list)
    work_experiences: List[WorkExperienceLenient] = Field(default_factory=list)
    skills: List[SkillLenient] = Field(default_factory=list)
    projects: List[ProjectLenient] = Field(default_factory=list)
    certificates: List[CertificateLenient] = Field(default_factory=list)
    languages: List[LanguageLenient] = Field(default_factory=list)
    custom_sections: List[CustomSectionLenient] = Field(default_factory=list)

    @field_validator(
        "education", "work_experiences", "projects", "certificates", mode="before"
    )
    @classmethod
    def ensure_start_dates(cls, v: Any) -> Any:
        if not isinstance(v, list):
            return v
        for item in v:
            if not isinstance(item, dict):
                continue
            
            # 1. Normalize dates
            # Start/Issue date
            if "start_date" in item:
                item["start_date"] = normalize_date_str(item.get("start_date")) or "1900-01-01"
            elif "issue_date" in item:
                item["issue_date"] = normalize_date_str(item.get("issue_date")) or "1900-01-01"
                
            # End/Expiration date
            if "end_date" in item:
                item["end_date"] = normalize_date_str(item.get("end_date"))
            elif "expiration_date" in item:
                item["expiration_date"] = normalize_date_str(item.get("expiration_date"))
                
            # 2. Chronological date alignment
            # For start/end dates
            if "start_date" in item and item.get("end_date"):
                try:
                    sd = datetime.strptime(item["start_date"], "%Y-%m-%d").date()
                    ed = datetime.strptime(item["end_date"], "%Y-%m-%d").date()
                    if ed < sd:
                        item["end_date"] = None
                except Exception:
                    pass
            # For issue/expiration dates
            if "issue_date" in item and item.get("expiration_date"):
                try:
                    sd = datetime.strptime(item["issue_date"], "%Y-%m-%d").date()
                    ed = datetime.strptime(item["expiration_date"], "%Y-%m-%d").date()
                    if ed < sd:
                        item["expiration_date"] = None
                except Exception:
                    pass
                    
            # 3. GPA cleaning
            if "gpa" in item:
                item["gpa"] = clean_gpa(item.get("gpa"))
                
            # 4. URL cleaning
            for url_field in ["url", "credential_url"]:
                if url_field in item:
                    item[url_field] = clean_url_str(item.get(url_field))

            # 5. Missing mandatory fields fallbacks
            for field in [
                "job_title",
                "company",
                "institution",
                "degree",
                "name",
                "issuing_organization",
            ]:
                if field in item and item[field] is None:
                    item[field] = f"Unknown {field.replace('_', ' ').title()}"
        return v


# ============================================================================
# Main Service
# ============================================================================


class PDFParserService:
    """Service for extracting and parsing PDF resumes using Docling and LLM"""

    def __init__(self):
        self.llm_service = LLMService()

        # Configure Docling for CPU
        pipeline_options = PdfPipelineOptions()
        pipeline_options.accelerator_options = AcceleratorOptions(device="cpu")
        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
        )
        logger.info("PDFParserService initialized with Docling (CPU)")

    async def _extract_text(self, pdf_path: str | Path) -> str:
        """Extract Markdown text from PDF using Docling"""

        def blocking_convert():
            result = self.converter.convert(str(pdf_path))
            return result.document.export_to_markdown()

        try:
            return await asyncio.to_thread(blocking_convert)
        except Exception as e:
            logger.error(f"Docling extraction failed: {e}")
            return ""

    async def parse_cv_structure(self, file_path: str) -> Dict[str, Any]:
        """Convert PDF to structured JSON using Docling + LLM"""
        try:
            # 1. Text Extraction
            raw_text = await self._extract_text(file_path)
            if not raw_text or len(raw_text.strip()) < 50:
                logger.warning("Extracted text is too short for reliable parsing.")

            # 2. LLM Structured Parsing
            logger.info("Sending text to LLM for structured extraction...")
            resume_data = await self.llm_service.parse_to_model_with_function_calling(
                text=raw_text,
                model_class=ResumeDataLenient,
                instructions=self._get_instructions(),
                tool_name="extract_resume",
            )

            # 3. Final cleanup and conversion
            return self._finalize_data(resume_data)

        except Exception as e:
            logger.error(f"Critical error in parse_cv_structure: {e}", exc_info=True)
            return self._get_empty_structure()

    def _get_instructions(self) -> str:
        return """You are an expert resume parser. Extract information from the provided text into the structured schema.

RULES:
1. Extraction: Capture all work experience, education, skills, certificates, languages, and projects. 
2. Headings: Be typo-tolerant with section headings (e.g., 'WORKEXPERIENCE' is 'work_experiences').
3. Logic: Match 'floating' dates to their corresponding jobs or projects. Handle table-formatted education/experience by reading across rows.
4. No Duplication: Extract each piece of information only once. Do not repeat data in multiple sections.
5. Missing Data: If a mandatory field (like job title or institution) is missing, use "Unknown". If a date is missing, use "1900-01-01".
6. Thoroughness: Include all bullet points and details for experiences and projects.
7. Custom Sections: Use for content that doesn't fit the standard categories.

Extract every detail accurately."""

    def _finalize_data(self, data: ResumeDataLenient) -> Dict[str, Any]:
        """Convert Pydantic model to dict, ensuring all lists exist and dates are strings"""
        # model_dump with mode='json' handles date serialization automatically
        raw_dict = data.model_dump(mode="json")

        # Ensure top-level keys exist for the consumer
        structure = self._get_empty_structure()
        structure.update(raw_dict)

        # Add a flag to indicate some fields might be placeholders
        structure["parsing_notes"] = (
            "Data extracted with LLM. Some missing fields filled with 'Unknown'."
        )

        return structure

    def _get_empty_structure(self) -> Dict[str, Any]:
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
