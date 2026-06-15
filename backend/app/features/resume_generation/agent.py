import logging
import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from uuid import uuid4
from sqlalchemy.ext.asyncio import AsyncSession

from features.resume_generation.schemas import GenerateResponse, GenerateRequest, JDAnalysis
from features.resume_generation.tools.assembler import AssemblerTool, DraftData
from features.profiles.repository import ProfileRepository
from features.profiles.models import Profile
from features.job_descriptions.service import JobDescriptionService
from features.job_descriptions.schemas import JobDescriptionCreate
from features.resumes.resume_drafts.service import ResumeDraftService
from features.resumes.resume_drafts.schemas import ResumeDraftCreate
from features.indexing.repository import EmbeddingRepository
from features.indexing.service import EmbeddingService

logger = logging.getLogger(__name__)


@dataclass
class GenerationContext:
    profile_uuid: str
    jd_text: str
    user_id: int

    profile: Optional[Profile] = None
    profile_id: Optional[int] = None
    jd_analysis: Optional[JDAnalysis] = None
    jd_embedding: Optional[List[float]] = None

    experiences: List = field(default_factory=list)
    education: List = field(default_factory=list)
    skills: List = field(default_factory=list)
    projects: List = field(default_factory=list)
    certificates: List = field(default_factory=list)
    languages: List = field(default_factory=list)
    summaries: List = field(default_factory=list)
    links: List = field(default_factory=list)
    custom_sections: List = field(default_factory=list)
    entity_embeddings: Dict[str, List[float]] = field(default_factory=dict)

    ranked_experiences: List[Dict] = field(default_factory=list)
    ranked_education: List[Dict] = field(default_factory=list)
    ranked_skills: List[Dict] = field(default_factory=list)
    ranked_projects: List[Dict] = field(default_factory=list)
    ranked_certificates: List[Dict] = field(default_factory=list)
    ranked_languages: List[Dict] = field(default_factory=list)

    draft_data: Optional[DraftData] = None
    draft_uuid: Optional[Any] = None


class ResumeGenerationAgent:
    def __init__(
        self,
        db: AsyncSession,
        profile_repo: ProfileRepository,
        jd_service: JobDescriptionService,
        draft_service: ResumeDraftService,
        embedding_repo: EmbeddingRepository,
        section_repos: Dict[str, Any],
        tools: Dict[str, Any],
    ):
        self.db = db
        self.profile_repo = profile_repo
        self.jd_service = jd_service
        self.draft_service = draft_service
        self.embedding_repo = embedding_repo
        self.section_repos = section_repos
        self.tools = tools

    async def run(
        self, profile_uuid: str, request: GenerateRequest, user_id: int
    ) -> GenerateResponse:
        ctx = GenerationContext(
            profile_uuid=profile_uuid,
            jd_text=request.job_description_text,
            user_id=user_id,
        )

        steps = [
            ("Load profile", self._step_load_profile),
            ("Save job description", self._step_save_jd),
            ("Analyze JD", self._step_analyze_jd),
            ("Embed JD text", self._step_embed_jd),
            ("Load all profile data", self._step_load_data),
            ("Load entity embeddings", self._step_load_embeddings),
            ("Hybrid search ranking", self._step_rank),
            ("Assemble draft data", self._step_assemble),
            ("Tailor content to job", self._step_tailor),
            ("Format content", self._step_format),
            ("Save resume draft", self._step_save_draft),
        ]

        for step_name, step_fn in steps:
            logger.info("[REASON] %s", step_name)
            await step_fn(ctx)
            logger.info("[OBSERVE] %s — OK", step_name)

        return GenerateResponse(draft_uuid=ctx.draft_uuid)

    async def _step_load_profile(self, ctx: GenerationContext) -> None:
        ctx.profile = await self.profile_repo.get_by_uuid(ctx.profile_uuid)
        if not ctx.profile:
            raise ValueError(f"Profile {ctx.profile_uuid} not found")
        if ctx.profile.user_id != ctx.user_id:
            raise ValueError("Access denied to this profile")
        ctx.profile_id = ctx.profile.id

    async def _step_save_jd(self, ctx: GenerationContext) -> None:
        jd_data = JobDescriptionCreate(
            title="Manual Entry",
            company="Manual Entry",
            url=f"https://paste.example.com/{uuid4()}",
            content=ctx.jd_text[:50000],
        )
        await self.jd_service.create_job_description(ctx.user_id, jd_data)

    async def _step_analyze_jd(self, ctx: GenerationContext) -> None:
        ctx.jd_analysis = await self.tools["analyze_jd"].analyze(ctx.jd_text)
        if not ctx.jd_analysis.required_skills and not ctx.jd_analysis.industry_keywords:
            logger.warning("[OBSERVE] Sparse JD analysis — no skills or keywords extracted")

    async def _step_embed_jd(self, ctx: GenerationContext) -> None:
        from worker.tasks.generation import embed_text_task
        loop = asyncio.get_running_loop()
        task = embed_text_task.delay(ctx.jd_text)
        ctx.jd_embedding = await loop.run_in_executor(
            None, lambda: task.get(timeout=60, propagate=True, interval=0.5)
        )

    async def _step_load_data(self, ctx: GenerationContext) -> None:
        pid = ctx.profile_id
        ctx.experiences = await self.section_repos["work_experience"].get_by_profile_id(pid)
        ctx.education = await self.section_repos["education"].get_by_profile_id(pid)
        ctx.skills = await self.section_repos["skill"].get_by_profile_id(pid)
        ctx.projects = await self.section_repos["project"].get_by_profile_id(pid)
        ctx.certificates = await self.section_repos["certificate"].get_by_profile_id(pid)
        ctx.languages = await self.section_repos["language"].get_by_profile_id(pid)
        ctx.summaries = await self.section_repos["summary"].get_all_by_profile_id(pid)
        ctx.links = await self.section_repos["link"].get_by_profile_id(pid)
        ctx.custom_sections = await self.section_repos["custom_section"].get_by_profile_id(pid)

    async def _step_load_embeddings(self, ctx: GenerationContext) -> None:
        entity_uuids = []
        for items in [ctx.experiences, ctx.education, ctx.projects, ctx.certificates]:
            entity_uuids.extend([str(e.uuid) for e in items])
        ctx.entity_embeddings = {}
        for euid in entity_uuids:
            found = await self.embedding_repo.find_by_entity(euid, embedding_type="full_text")
            for emb in found:
                if emb.vector_data is not None:
                    ctx.entity_embeddings[str(emb.entity_uuid)] = emb.vector_data
                    break

    async def _step_rank(self, ctx: GenerationContext) -> None:
        hs = self.tools["hybrid_search"]

        def sim(ent) -> float:
            vec = ctx.entity_embeddings.get(str(ent.uuid))
            if vec is not None and ctx.jd_embedding is not None:
                return EmbeddingService.calculate_cosine_similarity(vec, ctx.jd_embedding)
            return 0.0

        exp_sim = {str(e.uuid): sim(e) for e in ctx.experiences}
        edu_sim = {str(e.uuid): sim(e) for e in ctx.education}
        proj_sim = {str(p.uuid): sim(p) for p in ctx.projects}
        cert_sim = {str(c.uuid): sim(c) for c in ctx.certificates}

        ctx.ranked_experiences = hs.rank_work_experiences(ctx.experiences, ctx.jd_analysis, exp_sim)
        ctx.ranked_education = hs.rank_education(ctx.education, ctx.jd_analysis, edu_sim)
        ctx.ranked_skills = hs.rank_skills(ctx.skills, ctx.jd_analysis)
        ctx.ranked_projects = hs.rank_projects(ctx.projects, ctx.jd_analysis, proj_sim)
        ctx.ranked_certificates = hs.rank_certificates(ctx.certificates, ctx.jd_analysis, cert_sim)
        ctx.ranked_languages = hs.rank_languages(ctx.languages, ctx.jd_analysis)

    async def _step_tailor(self, ctx: GenerationContext) -> None:
        if ctx.draft_data is None:
            return
        ctx.draft_data = await self.tools["tailor"].tailor_draft(ctx.draft_data, ctx.jd_analysis)

    async def _step_format(self, ctx: GenerationContext) -> None:
        if ctx.draft_data is None:
            return
        ctx.draft_data = self.tools["format"].format_draft(ctx.draft_data)

    async def _step_assemble(self, ctx: GenerationContext) -> None:
        profile_dict = {
            "name": ctx.profile.name,
            "email": ctx.profile.email,
            "phone_number": ctx.profile.phone_number,
            "location": ctx.profile.location,
        }
        ctx.draft_data = self.tools["assemble"].assemble(
            profile_data=profile_dict,
            ranked_experiences=ctx.ranked_experiences[:5],
            ranked_education=ctx.ranked_education[:3],
            ranked_skills=ctx.ranked_skills,
            ranked_projects=ctx.ranked_projects[:3],
            ranked_certificates=ctx.ranked_certificates[:3],
            ranked_languages=ctx.ranked_languages,
            summaries=ctx.summaries,
            links=ctx.links,
            custom_sections=ctx.custom_sections,
        )
        issues = AssemblerTool.validate(ctx.draft_data)
        if issues:
            logger.warning("[OBSERVE] Draft validation issues: %s", issues)

    async def _step_save_draft(self, ctx: GenerationContext) -> None:
        raw_title = ctx.jd_analysis.job_title_raw or "Unknown Position"
        raw_company = ctx.jd_analysis.company_raw or "Unknown Company"
        title = f"Generated — {raw_title} @ {raw_company}"
        create_data = ResumeDraftCreate(
            title=title,
            template_name="CANADIAN",
            draft_data=ctx.draft_data.model_dump(),
        )
        result = await self.draft_service.create_draft(ctx.profile_id, create_data)
        ctx.draft_uuid = result.uuid
