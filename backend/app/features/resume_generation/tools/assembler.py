import logging
from typing import Any, Dict, List
from datetime import date
import uuid as py_uuid
from pydantic import BaseModel, Field
from typing import Optional

logger = logging.getLogger(__name__)


class BasicInfo(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    location: str = ""


class WorkExperienceItem(BaseModel):
    uuid: str = ""
    job_title: str = ""
    company: str = ""
    description: str = ""
    start_date: str = ""
    end_date: str = ""


class EducationItem(BaseModel):
    uuid: str = ""
    institution: str = ""
    degree: str = ""
    field_of_study: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
    description: Optional[str] = None
    gpa: Optional[str] = None


class SkillItem(BaseModel):
    uuid: str = ""
    name: str = ""
    category: Optional[str] = None
    proficiency: Optional[str] = None


class ProjectItem(BaseModel):
    uuid: str = ""
    name: str = ""
    description: Optional[str] = None
    technologies: Optional[str] = None
    start_date: str = ""
    end_date: str = ""
    url: Optional[str] = None


class CertificateItem(BaseModel):
    uuid: str = ""
    name: str = ""
    issuing_organization: str = ""
    issue_date: str = ""
    expiration_date: Optional[str] = None
    credential_id: Optional[str] = None


class LanguageItem(BaseModel):
    uuid: str = ""
    language: str = ""
    proficiency: str = ""


class CustomSectionItem(BaseModel):
    uuid: str = ""
    title: str = ""
    content: str = ""


class LinkItem(BaseModel):
    uuid: str = ""
    label: str = ""
    url: str = ""
    platform: str = ""
    is_visible: bool = True


class ProfileData(BaseModel):
    basicInfo: BasicInfo = Field(default_factory=BasicInfo)
    summary: str = ""
    workExperiences: List[WorkExperienceItem] = Field(default_factory=list)
    education: List[EducationItem] = Field(default_factory=list)
    skills: List[SkillItem] = Field(default_factory=list)
    projects: List[ProjectItem] = Field(default_factory=list)
    certificates: List[CertificateItem] = Field(default_factory=list)
    languages: List[LanguageItem] = Field(default_factory=list)
    customSections: List[CustomSectionItem] = Field(default_factory=list)
    links: List[LinkItem] = Field(default_factory=list)
    skillUseCategories: bool = False


class ComponentDef(BaseModel):
    uuid: str = ""
    component_type: str = ""
    component_id: int = 0
    is_included: bool = True
    order_index: int = 0


class DraftData(BaseModel):
    components: List[ComponentDef] = Field(default_factory=list)
    profileData: ProfileData = Field(default_factory=ProfileData)
    selectedTemplate: str = "CANADIAN"


class AssemblerTool:
    @staticmethod
    def _format_date(d: Any) -> str:
        if isinstance(d, date):
            return d.isoformat()
        if d:
            return str(d)
        return ""

    @staticmethod
    def _uuid_from_entity(entity: Any) -> str:
        return str(getattr(entity, "uuid", py_uuid.uuid4()))

    def assemble(
        self,
        profile_data: Dict[str, Any],
        ranked_experiences: List,
        ranked_education: List,
        ranked_skills: List,
        ranked_projects: List,
        ranked_certificates: List,
        ranked_languages: List,
        summaries: List,
        links: List,
        custom_sections: List,
        tailored_summary: str = "",
    ) -> DraftData:
        components = []
        next_order = 0

        section_types = [
            "professional_summary",
            "work_experience",
            "education",
            "skills",
            "projects",
            "certificates",
            "languages",
            "custom_sections",
        ]
        for st in section_types:
            components.append(
                ComponentDef(
                    uuid=str(py_uuid.uuid4()),
                    component_type=st,
                    order_index=next_order,
                )
            )
            next_order += 1

        if not tailored_summary:
            for s in summaries:
                content = getattr(s, "content", None) or getattr(s, "summary", "")
                if content:
                    tailored_summary = content
                    break

        profile = ProfileData(
            basicInfo=BasicInfo(
                name=profile_data.get("name", ""),
                email=profile_data.get("email", ""),
                phone=profile_data.get("phone_number", ""),
                location=profile_data.get("location", ""),
            ),
            summary=tailored_summary,
            workExperiences=[
                WorkExperienceItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    job_title=getattr(r["entity"], "job_title", ""),
                    company=getattr(r["entity"], "company", ""),
                    description=getattr(r["entity"], "description", ""),
                    start_date=self._format_date(getattr(r["entity"], "start_date", None)),
                    end_date=self._format_date(getattr(r["entity"], "end_date", None)),
                )
                for r in ranked_experiences
            ],
            education=[
                EducationItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    institution=getattr(r["entity"], "institution", ""),
                    degree=getattr(r["entity"], "degree", ""),
                    field_of_study=getattr(r["entity"], "field_of_study", None),
                    start_date=self._format_date(getattr(r["entity"], "start_date", None)),
                    end_date=self._format_date(getattr(r["entity"], "end_date", None)),
                    description=getattr(r["entity"], "description", None),
                    gpa=getattr(r["entity"], "gpa", None),
                )
                for r in ranked_education
            ],
            skills=[
                SkillItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    name=getattr(r["entity"], "name", ""),
                    category=getattr(r["entity"], "category", None),
                    proficiency=getattr(r["entity"], "proficiency", None),
                )
                for r in ranked_skills
            ],
            projects=[
                ProjectItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    name=getattr(r["entity"], "name", ""),
                    description=getattr(r["entity"], "description", None),
                    technologies=getattr(r["entity"], "technologies", None),
                    start_date=self._format_date(getattr(r["entity"], "start_date", None)),
                    end_date=self._format_date(getattr(r["entity"], "end_date", None)),
                    url=getattr(r["entity"], "url", None),
                )
                for r in ranked_projects
            ],
            certificates=[
                CertificateItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    name=getattr(r["entity"], "name", ""),
                    issuing_organization=getattr(r["entity"], "issuing_organization", ""),
                    issue_date=self._format_date(getattr(r["entity"], "issue_date", None)),
                )
                for r in ranked_certificates
            ],
            languages=[
                LanguageItem(
                    uuid=self._uuid_from_entity(r["entity"]),
                    language=getattr(r["entity"], "language", ""),
                    proficiency=getattr(r["entity"], "proficiency", ""),
                )
                for r in ranked_languages
            ],
            customSections=[
                CustomSectionItem(
                    uuid=self._uuid_from_entity(cs),
                    title=getattr(cs, "title", ""),
                    content=getattr(cs, "content", ""),
                )
                for cs in custom_sections
            ],
            links=[
                LinkItem(
                    uuid=self._uuid_from_entity(link),
                    label=getattr(link, "label", ""),
                    url=getattr(link, "url", ""),
                    platform=getattr(link, "platform", ""),
                    is_visible=getattr(link, "is_visible", True),
                )
                for link in links
            ],
            skillUseCategories=False,
        )

        return DraftData(components=components, profileData=profile)

    @staticmethod
    def validate(draft: DraftData) -> List[str]:
        issues = []
        if not draft.profileData.basicInfo.name:
            issues.append("Missing name in basicInfo")
        return issues
