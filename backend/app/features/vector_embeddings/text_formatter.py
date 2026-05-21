"""Text extraction and formatting for embedding generation."""
from typing import Optional
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
        """
        Format skill for embedding.
        Per planning: use title only for now, description to be added later.
        """
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
        """
        Extract a preview of text for storage in database.

        Args:
            text: Full text
            max_chars: Maximum characters to keep

        Returns:
            Preview text
        """
        if not text:
            return ""
        return text[:max_chars] + ("..." if len(text) > max_chars else "")
