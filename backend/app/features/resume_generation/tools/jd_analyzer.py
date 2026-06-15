import logging
from features.llm.service import LLMService
from features.resume_generation.schemas import JDAnalysis

logger = logging.getLogger(__name__)


class JDAnalyzerTool:
    def __init__(self, llm_service: LLMService):
        self.llm = llm_service

    async def analyze(self, jd_text: str) -> JDAnalysis:
        instructions = (
            "You are an expert job description analyst. Extract structured information "
            "from the following job description. Be thorough — identify every required "
            "and preferred skill, qualification, and responsibility listed. "
            "Extract the job title and company name if they appear in the text."
        )

        prompt = f"--- Job Description Text ---\n{jd_text}"

        try:
            result = await self.llm.parse_to_model_with_function_calling(
                text=prompt,
                model_class=JDAnalysis,
                instructions=instructions,
                tool_name="analyze_job_description",
            )
            return result
        except Exception as e:
            logger.error(f"JD analysis failed: {e}")
            return JDAnalysis(industry_keywords=[w for w in jd_text.split() if len(w) > 3][:50])
