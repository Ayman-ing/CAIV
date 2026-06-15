import logging
from sqlalchemy.ext.asyncio import AsyncSession
from features.profiles.repository import ProfileRepository
from features.profiles.work_experiences.repository import WorkExperienceRepository
from features.profiles.education.repository import EducationRepository
from features.profiles.skills.repository import SkillRepository
from features.profiles.projects.repository import ProjectRepository
from features.profiles.certificates.repository import CertificateRepository
from features.profiles.languages.repository import LanguageRepository
from features.profiles.professional_summaries.repository import ProfessionalSummaryRepository
from features.profiles.profile_links.repository import ProfileLinkRepository
from features.profiles.custom_sections.repository import CustomSectionRepository
from features.job_descriptions.repository import JobDescriptionRepository
from features.job_descriptions.service import JobDescriptionService
from features.resumes.resume_drafts.repository import ResumeDraftRepository
from features.resumes.resume_drafts.service import ResumeDraftService
from features.indexing.repository import EmbeddingRepository
from features.resume_generation.schemas import GenerateRequest, GenerateResponse
from features.resume_generation.agent import ResumeGenerationAgent
from features.resume_generation.tools.jd_analyzer import JDAnalyzerTool
from features.resume_generation.tools.hybrid_search import HybridSearchTool
from features.resume_generation.tools.tailor import TailorTool
from features.resume_generation.tools.assembler import AssemblerTool
from features.resume_generation.tools.formatter import FormattingTool
from features.llm.service import LLMService

logger = logging.getLogger(__name__)


class ResumeGenerationService:
    def __init__(self, db: AsyncSession):
        self.db = db

    def _build_agent(self) -> ResumeGenerationAgent:
        llm = LLMService()
        tools = {
            "analyze_jd": JDAnalyzerTool(llm),
            "hybrid_search": HybridSearchTool(),
            "tailor": TailorTool(llm),
            "assemble": AssemblerTool(),
            "format": FormattingTool(),
        }
        section_repos = {
            "work_experience": WorkExperienceRepository(self.db),
            "education": EducationRepository(self.db),
            "skill": SkillRepository(self.db),
            "project": ProjectRepository(self.db),
            "certificate": CertificateRepository(self.db),
            "language": LanguageRepository(self.db),
            "summary": ProfessionalSummaryRepository(self.db),
            "link": ProfileLinkRepository(self.db),
            "custom_section": CustomSectionRepository(self.db),
        }
        return ResumeGenerationAgent(
            db=self.db,
            profile_repo=ProfileRepository(self.db),
            jd_service=JobDescriptionService(JobDescriptionRepository(self.db)),
            draft_service=ResumeDraftService(ResumeDraftRepository(self.db)),
            embedding_repo=EmbeddingRepository(self.db),
            section_repos=section_repos,
            tools=tools,
        )

    async def generate(
        self, profile_uuid: str, request: GenerateRequest, user_id: int
    ) -> GenerateResponse:
        agent = self._build_agent()
        return await agent.run(profile_uuid, request, user_id)
