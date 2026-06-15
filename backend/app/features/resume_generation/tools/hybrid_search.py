import logging
from typing import List, Dict, Any
from features.resume_generation.schemas import JDAnalysis

logger = logging.getLogger(__name__)

RRF_K = 10


class HybridSearchTool:
    @staticmethod
    def score_entity_text(text: str, analysis: JDAnalysis) -> float:
        if not text:
            return 0.0
        text_lower = text.lower()
        score = 0.0
        keywords = (
            analysis.required_skills
            + analysis.preferred_skills
            + analysis.industry_keywords
            + [kw.strip().lower() for kw in analysis.key_responsibilities]
            + analysis.qualifications
        )
        for kw in keywords:
            if kw.lower() in text_lower:
                score += 1.0
        if analysis.required_experience:
            exp_terms = analysis.required_experience.lower().split()
            for term in exp_terms:
                if term in text_lower:
                    score += 0.5
        return score

    @staticmethod
    def _rrf(keyword_rank: int, vector_rank: int, k: int = RRF_K) -> float:
        return (1.0 / (k + keyword_rank)) + (1.0 / (k + vector_rank))

    def _rank_hybrid(
        self,
        entities: List[Any],
        analysis: JDAnalysis,
        similarities: Dict[str, float],
        text_fn,
    ) -> List[Dict[str, Any]]:
        if not entities:
            return []

        kw_scores = {}
        for ent in entities:
            uid = str(ent.uuid)
            kw_scores[uid] = self.score_entity_text(text_fn(ent), analysis)

        kw_ranked = sorted(entities, key=lambda e: kw_scores.get(str(e.uuid), 0), reverse=True)
        kw_ranks = {str(e.uuid): i for i, e in enumerate(kw_ranked)}

        vec_ranked = sorted(entities, key=lambda e: similarities.get(str(e.uuid), 0), reverse=True)
        vec_ranks = {str(e.uuid): i for i, e in enumerate(vec_ranked)}

        n = len(entities)
        scored = []
        for ent in entities:
            uid = str(ent.uuid)
            combined = self._rrf(
                kw_ranks.get(uid, n - 1),
                vec_ranks.get(uid, n - 1),
            )
            scored.append({"entity": ent, "score": round(combined, 4), "uuid": uid})

        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def rank_work_experiences(
        self, experiences: List[Any], analysis: JDAnalysis, similarities: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        return self._rank_hybrid(
            experiences, analysis, similarities,
            lambda e: f"{e.job_title} {e.company} {e.description or ''}",
        )

    def rank_education(
        self, education: List[Any], analysis: JDAnalysis, similarities: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        return self._rank_hybrid(
            education, analysis, similarities,
            lambda e: f"{e.degree} {e.field_of_study or ''} {e.institution} {e.description or ''}",
        )

    def rank_projects(
        self, projects: List[Any], analysis: JDAnalysis, similarities: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        return self._rank_hybrid(
            projects, analysis, similarities,
            lambda e: f"{e.name} {e.description or ''} {e.technologies or ''}",
        )

    def rank_certificates(
        self, certificates: List[Any], analysis: JDAnalysis, similarities: Dict[str, float]
    ) -> List[Dict[str, Any]]:
        return self._rank_hybrid(
            certificates, analysis, similarities,
            lambda e: f"{e.name} {e.issuing_organization or ''}",
        )

    def rank_skills(self, skills: List[Any], analysis: JDAnalysis) -> List[Dict[str, Any]]:
        scored = []
        required_set = {s.lower() for s in analysis.required_skills}
        preferred_set = {s.lower() for s in analysis.preferred_skills}
        for skill in skills:
            text = f"{skill.name} {skill.category or ''}"
            kw_score = self.score_entity_text(text, analysis)
            bonus = 2.0 if skill.name.lower() in required_set else (1.0 if skill.name.lower() in preferred_set else 0.0)
            scored.append({"entity": skill, "score": kw_score + bonus, "uuid": str(skill.uuid)})
        scored.sort(key=lambda x: x["score"], reverse=True)
        return scored

    def rank_languages(self, languages: List[Any], analysis: JDAnalysis) -> List[Dict[str, Any]]:
        scored = []
        for lang in languages:
            kw_score = self.score_entity_text(lang.language, analysis)
            scored.append({"entity": lang, "score": kw_score, "uuid": str(lang.uuid)})
        return sorted(scored, key=lambda x: x["score"], reverse=True)
