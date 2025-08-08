# Import all feature modules
from .users import router as users_router
from .work_experiences import router as work_experiences_router
from .projects import router as projects_router
from .skills import router as skills_router
from .education import router as education_router
from .certificates import router as certificates_router
from .languages import language_router
from .resumes import resume_router
from .profiles import profile_router
from .custom_sections import custom_section_router
from .user_links import user_link_router
from .job_descriptions import job_description_router

# List of all feature routers
feature_routers = [
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
    user_link_router,
    job_description_router,
]

__all__ = ["feature_routers"]
