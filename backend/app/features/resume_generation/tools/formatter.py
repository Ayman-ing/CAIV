import re
import logging
from features.resume_generation.tools.assembler import DraftData

logger = logging.getLogger(__name__)

BULLET_CHAR = "•"
LIST_MARKERS = re.compile(r"^[\s]*[-*•]\s+", re.MULTILINE)

def normalize_bullets(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""

    has_any_marker = bool(LIST_MARKERS.search(stripped))
    if has_any_marker:
        lines = stripped.split("\n")
        result = []
        for line in lines:
            trimmed = line.strip()
            if not trimmed:
                result.append("")
                continue
            normalized = LIST_MARKERS.sub(f"{BULLET_CHAR} ", trimmed)
            if not normalized.startswith(BULLET_CHAR):
                result.append(trimmed)
            else:
                result.append(normalized)
        out = "\n".join(result)
        return out.strip()

    return _bulletize_paragraph(stripped)


def _bulletize_paragraph(text: str) -> str:
    text = text.replace("\n", " ").strip()
    while "  " in text:
        text = text.replace("  ", " ")

    bulletized = _split_into_sentences(text)
    if len(bulletized) <= 1:
        return text

    out_lines = [f"{BULLET_CHAR} {s}" for s in bulletized]
    return "\n".join(out_lines)


def _split_into_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    result = []
    for p in parts:
        p = p.strip()
        if p:
            result.append(p)
    return result


def clean_text(text: str | None) -> str:
    if not text:
        return ""
    text = text.strip()
    lines = text.split("\n")
    cleaned = [ln.rstrip() for ln in lines]
    out = "\n".join(cleaned)
    while "\n\n\n" in out:
        out = out.replace("\n\n\n", "\n\n")
    return out.strip()


class FormattingTool:
    @staticmethod
    def format_draft(draft: DraftData) -> DraftData:
        pd = draft.profileData

        if pd.summary:
            pd.summary = clean_text(pd.summary)

        for exp in pd.workExperiences:
            if exp.description:
                exp.description = normalize_bullets(exp.description)

        for edu in pd.education:
            if edu.description:
                edu.description = normalize_bullets(edu.description)

        for proj in pd.projects:
            if proj.description:
                proj.description = normalize_bullets(proj.description)

        for cs in pd.customSections:
            if cs.content:
                cs.content = clean_text(cs.content)

        return draft
