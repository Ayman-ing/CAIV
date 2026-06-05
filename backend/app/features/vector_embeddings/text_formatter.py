"""Text extraction and formatting for embedding generation."""
from typing import Optional, List, Tuple, Callable
import logging

logger = logging.getLogger(__name__)


class TextFormatter:
    """Formats various profile entities into text for embedding."""

    @staticmethod
    def format_work_experience(
        title: str,
        company: str,
        description: Optional[str] = None,
    ) -> str:
        """Format work experience for embedding."""
        parts = [f"{title} at {company}"]
        if description:
            parts.append(description)
        return " ".join(parts)

    @staticmethod
    def format_education(
        degree: str,
        field: str,
        school: str,
        description: Optional[str] = None,
    ) -> str:
        """Format education for embedding."""
        parts = [f"{degree} in {field} from {school}"]
        if description:
            parts.append(description)
        return " ".join(parts)

    @staticmethod
    def format_project(
        name: str,
        description: Optional[str] = None,
        technologies: Optional[str] = None,
    ) -> str:
        """Format project for embedding."""
        parts = [f"Project: {name}"]
        if description:
            parts.append(description)
        if technologies:
            parts.append(f"Technologies: {technologies}")
        return " ".join(parts)

    @staticmethod
    def format_skill(
        name: str,
        category: Optional[str] = None,
        proficiency: Optional[str] = None,
        years_experience: Optional[int] = None,
    ) -> str:
        """Format skill for embedding."""
        parts = [name]
        if category:
            parts.append(f"({category})")
        if proficiency:
            parts.append(f"[{proficiency}]")
        if years_experience:
            years_text = "year" if years_experience == 1 else "years"
            parts.append(f"{years_experience} {years_text}")
        return " ".join(parts)

    @staticmethod
    def format_language(
        language: str,
        proficiency: Optional[str] = None,
        can_read: Optional[bool] = None,
        can_write: Optional[bool] = None,
        can_speak: Optional[bool] = None,
    ) -> str:
        """Format language skill for embedding."""
        parts = [language]
        if proficiency:
            parts.append(f"({proficiency})")

        skills = []
        if can_read:
            skills.append("read")
        if can_write:
            skills.append("write")
        if can_speak:
            skills.append("speak")

        if skills:
            parts.append(f"[{', '.join(skills)}]")

        return " ".join(parts)

    @staticmethod
    def format_certificate(
        name: str,
        issuing_organization: Optional[str] = None,
        credential_id: Optional[str] = None,
    ) -> str:
        """Format certificate for embedding."""
        parts = [f"Certificate: {name}"]
        if issuing_organization:
            parts.append(f"from {issuing_organization}")
        if credential_id:
            parts.append(f"(ID: {credential_id})")
        return " ".join(parts)

    @staticmethod
    def format_professional_summary(
        content: str,
        title: Optional[str] = None,
    ) -> str:
        """Format professional summary for embedding."""
        parts = []
        if title:
            parts.append(f"{title}:")
        parts.append(content)
        return " ".join(parts)

    @staticmethod
    def format_custom_section(
        content: str,
        title: Optional[str] = None,
    ) -> str:
        """Format custom section for embedding."""
        parts = []
        if title:
            parts.append(f"{title}:")
        parts.append(content)
        return " ".join(parts)

    @staticmethod
    def extract_text_preview(text: str, max_chars: int = 200) -> str:
        """Extract a preview of text for storage in database."""
        if not text:
            return ""
        return text[:max_chars] + ("..." if len(text) > max_chars else "")

    @staticmethod
    def get_sections_config() -> List[Tuple[type, Callable, str]]:
        """
        Return the list of (model_class, text_formatter_fn, section_name) for all indexed entity types.

        Imported lazily to avoid circular imports. ProfileLinks are excluded
        intentionally — they carry no semantic value for vector matching.
        """
        from features.profiles.professional_summaries.models import ProfessionalSummary
        from features.profiles.work_experiences.models import WorkExperience
        from features.profiles.skills.models import Skill
        from features.profiles.projects.models import Project
        from features.profiles.education.models import Education
        from features.profiles.certificates.models import Certificate
        from features.profiles.languages.models import Language
        from features.profiles.custom_sections.models import CustomSection

        return [
            (
                ProfessionalSummary,
                lambda r: TextFormatter.format_professional_summary(
                    content=r.content or "",
                    title=r.title,
                ),
                "professional_summaries",
            ),
            (
                WorkExperience,
                lambda r: TextFormatter.format_work_experience(
                    title=r.job_title or "",
                    company=r.company or "",
                    description=r.description,
                ),
                "work_experiences",
            ),
            (
                Project,
                lambda r: TextFormatter.format_project(
                    name=r.name or "",
                    description=r.description,
                    technologies=r.technologies,
                ),
                "projects",
            ),
            (
                Skill,
                lambda r: TextFormatter.format_skill(
                    name=r.name or "",
                    category=r.category,
                    proficiency=r.proficiency,
                    years_experience=r.years_experience,
                ),
                "skills",
            ),
            (
                Education,
                lambda r: TextFormatter.format_education(
                    degree=r.degree or "",
                    field=r.field_of_study or "",
                    school=r.institution or "",
                    description=r.description,
                ),
                "education",
            ),
            (
                Certificate,
                lambda r: TextFormatter.format_certificate(
                    name=r.name or "",
                    issuing_organization=r.issuing_organization,
                    credential_id=r.credential_id,
                ),
                "certificates",
            ),
            (
                Language,
                lambda r: TextFormatter.format_language(
                    language=r.language or "",
                    proficiency=r.proficiency,
                    can_read=r.can_read,
                    can_write=r.can_write,
                    can_speak=r.can_speak,
                ),
                "languages",
            ),
            (
                CustomSection,
                lambda r: TextFormatter.format_custom_section(
                    content=r.content or "",
                    title=r.title,
                ),
                "custom_sections",
            ),
        ]
