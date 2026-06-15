import logging
from features.llm.service import LLMService
from features.resume_generation.schemas import JDAnalysis, TailoredDraft
from features.resume_generation.tools.assembler import DraftData, WorkExperienceItem, ProjectItem

logger = logging.getLogger(__name__)

TAILOR_DRAFT_PROMPT = """You are a professional resume writer. Rephrase the following resume descriptions to better match the target job.

ABSOLUTE RULES — Violating any of these will get you fired:
1. NEVER add skills, technologies, tools, programming languages, or accomplishments that are not already in the original text. ZERO TOLERANCE.
2. NEVER change seniority level, years of experience, job titles, or specific claims.
3. ONLY rephrase existing content — you may reorder points, adjust wording for relevance, or emphasize things already present.
4. If a description is empty, leave it empty.
5. If a professional summary is empty, leave it empty.

The job context below is provided ONLY so you know which existing points to emphasize. It is NOT a list of things to add.

FORMATTING & CONSISTENCY:
6. Every work experience and project description must use bullet format — each point starts with "• " on its own line.
7. All bullets in a section must use the SAME verb tense:
   - (CURRENT) roles → present tense ("Lead", "Manage", "Develop")
   - (PAST) roles → past tense ("Led", "Managed", "Developed")
   - NEVER mix tenses within one section.
8. Parallel structure: every bullet in a section starts with a strong action verb in the same grammatical form.
9. Consistent punctuation: all bullets end with a period, or none do — pick one per section.

Target Job Context (for emphasis reference only — DO NOT add these to the content):
{job_context}

ORIGINAL CONTENT TO REPHRASE:
{content_blocks}

Respond with the tailored versions in the same order as provided."""


class TailorTool:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    def _build_context(self, analysis: JDAnalysis) -> str:
        return "\n".join([
            f"Job Title: {analysis.job_title_raw or 'N/A'}",
            f"Required Skills: {', '.join(analysis.required_skills)}",
            f"Preferred Skills: {', '.join(analysis.preferred_skills)}",
            f"Key Responsibilities: {', '.join(analysis.key_responsibilities)}",
            f"Qualifications: {', '.join(analysis.qualifications)}",
            f"Industry Keywords: {', '.join(analysis.industry_keywords)}",
        ])

    def _build_content_blocks(self, draft: DraftData) -> tuple[str, list[str], list[str]]:
        blocks = []
        summary = (draft.profileData.summary or "").strip()
        exp_originals = []
        proj_originals = []
        has_summary = False

        if summary:
            blocks.append(f"Professional Summary:\n{summary}")
            has_summary = True

        for i, exp in enumerate(draft.profileData.workExperiences):
            desc = (exp.description or "").strip()
            if desc:
                period_hint = "(CURRENT)" if exp.end_date in (None, "", "Present", "present") else "(PAST)"
                blocks.append(f"Work Experience {i+1} {period_hint}: {exp.job_title} @ {exp.company}\nDescription:\n{desc}")
                exp_originals.append(desc)

        for i, proj in enumerate(draft.profileData.projects):
            desc = (proj.description or "").strip()
            if desc:
                blocks.append(f"Project {i+1}: {proj.name}\nDescription:\n{desc}")
                proj_originals.append(desc)

        return "\n\n".join(blocks), exp_originals, proj_originals, has_summary

    async def tailor_draft(self, draft: DraftData, analysis: JDAnalysis) -> DraftData:
        job_context = self._build_context(analysis)
        content_blocks, exp_originals, proj_originals, has_summary = self._build_content_blocks(draft)

        if not exp_originals and not proj_originals and not has_summary:
            return draft

        prompt = TAILOR_DRAFT_PROMPT.format(job_context=job_context, content_blocks=content_blocks)
        try:
            result = await self.llm.parse_to_model_with_function_calling(
                text=prompt,
                model_class=TailoredDraft,
                instructions="You are a strict Resume Optimization Agent. You are only allowed to rewrite, reorder, or emphasize existing descriptionsfrom the User Context to match the Job Description. Do NOT invent companies, metrics, dates, skills, or projects or any information not grounded. If a skill is not present in the User Context, do not add it.Enforce consistent verb tense per section and uniform bullet format. Return items in the same order.", 
                tool_name="tailor_draft",
            )

            if has_summary:
                draft.profileData.summary = result.summary or draft.profileData.summary

            for i, desc in enumerate(result.experience_descriptions):
                if i < len(draft.profileData.workExperiences):
                    draft.profileData.workExperiences[i].description = desc or exp_originals[i]

            for i, desc in enumerate(result.project_descriptions):
                if i < len(draft.profileData.projects):
                    draft.profileData.projects[i].description = desc or proj_originals[i]

        except Exception as e:
            logger.warning(f"Draft tailoring failed, using original content: {e}")

        return draft
