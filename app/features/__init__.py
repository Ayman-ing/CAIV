# Import all feature modules
from .auth import auth_router  # Add this import
from .users import router as users_router
from .profiles.work_experiences import router as work_experiences_router
from .profiles.projects import router as projects_router
from .profiles.skills import router as skills_router
from .profiles.education import router as education_router
from .profiles.certificates import router as certificates_router
from .profiles.languages import language_router
from .resumes import resume_router
from .profiles import profile_router
from .profiles.custom_sections import custom_section_router
from .profiles.profile_links import profile_link_router
from .job_descriptions import job_description_router


# List of all feature routers
feature_routers = [
    auth_router,
    users_router,
    work_experiences_router,
    projects_router,
    skills_router,
    education_router,
    certificates_router,
    language_router,
    resume_router,
    profile_router,
    custom_section_router,
    profile_link_router,
    job_description_router,
]

__all__ = ["feature_routers"]
