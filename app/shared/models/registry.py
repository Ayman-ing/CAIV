# Import all models to register them with SQLAlchemy
from app.features.users.models import User
from app.features.profiles.work_experiences.models import WorkExperience
from app.features.profiles.education.models import Education
from app.features.profiles.skills.models import Skill
from app.features.profiles.projects.models import Project
from app.features.profiles.certificates.models import Certificate
from app.features.profiles.languages.models import Language
from app.features.profiles.models import Profile
from app.features.profiles.custom_sections.models import CustomSection
from app.features.profiles.profile_links.models import ProfileLink
from app.features.job_descriptions.models import JobDescription
from app.features.job_keywords.models import JobKeyword
from app.features.job_requirements.models import JobRequirement
from app.features.outbox_events.models import OutboxEvent
from app.features.profiles.professional_summaries.models import ProfessionalSummary
from app.features.vector_embeddings.models import VectorEmbedding
from app.features.resumes.models import GeneratedResume, ResumeComponent
from app.shared.models.base import Base

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
    "VectorEmbedding",
    
]
