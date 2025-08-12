from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from shared.models.base import Base

# Import all related models to ensure they're available for relationships
from .professional_summaries.models import ProfessionalSummary
from .work_experiences.models import WorkExperience
from .education.models import Education
from .projects.models import Project
from .skills.models import Skill
from .certificates.models import Certificate
from .languages.models import Language
from .profile_links.models import ProfileLink
from .custom_sections.models import CustomSection

# Import from other features
from features.resumes.models import GeneratedResume
from features.users.models import User

class Profile(Base):
    __tablename__ = 'profiles'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    name = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="profiles")
    generated_resumes = relationship("GeneratedResume", back_populates="profile")
    education = relationship("Education", back_populates="profile")
    work_experiences = relationship("WorkExperience", back_populates="profile")
    projects = relationship("Project", back_populates="profile")
    skills = relationship("Skill", back_populates="profile")
    certificates = relationship("Certificate", back_populates="profile")
    languages = relationship("Language", back_populates="profile")
    professional_summaries = relationship("ProfessionalSummary", back_populates="profile")
    profile_links = relationship("ProfileLink", back_populates="profile")
    custom_sections = relationship("CustomSection", back_populates="profile")