# Import all models to register them with SQLAlchemy
from features.users.models import User
from features.profiles.work_experiences.models import WorkExperience
from features.profiles.education.models import Education
from features.profiles.skills.models import Skill
from features.profiles.projects.models import Project
from features.profiles.certificates.models import Certificate
from features.profiles.languages.models import Language
from features.profiles.models import Profile
from features.profiles.custom_sections.models import CustomSection
from features.profiles.profile_links.models import ProfileLink
from features.job_descriptions.models import JobDescription
from features.job_keywords.models import JobKeyword
from features.job_requirements.models import JobRequirement
from features.outbox_events.models import OutboxEvent
from features.profiles.professional_summaries.models import ProfessionalSummary
from features.vector_embeddings.models import Embedding
from features.resumes.models import GeneratedResume, ResumeComponent
from shared.models.base import Base

# Export all models for easy import
__all__ = [
    "Base",
    "User",
    "Profile",
    "WorkExperience",
    "Education",
    "CustomSection",
    "ProfileLink",
    "JobDescription",
    "JobKeyword",
    "JobRequirement",
    "OutboxEvent",
    "ProfessionalSummary",
    "Skill",
    "Project",
    "Certificate",
    "Language",
    "GeneratedResume",
    "ResumeComponent",
    "Embedding",
    
]
