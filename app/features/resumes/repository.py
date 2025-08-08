"""
Resume Repository

Handles all database operations for resumes and resume components.
"""

from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from app.db.models.generated_resume import GeneratedResume
from app.db.models.resume_component import ResumeComponent
from app.features.resumes.schemas import GeneratedResumeCreate, GeneratedResumeUpdate, ResumeComponentCreate, ResumeComponentUpdate


class ResumeRepository:
    """Repository for resume database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_resume(self, user_id: int, resume_data: GeneratedResumeCreate) -> GeneratedResume:
        """Create a new resume"""
        db_resume = GeneratedResume(
            user_id=user_id,
            **resume_data.model_dump()
        )
        self.db.add(db_resume)
        self.db.commit()
        self.db.refresh(db_resume)
        return db_resume
    
    def get_resume_by_uuid(self, resume_uuid: str) -> Optional[GeneratedResume]:
        """Get resume by UUID with components"""
        return (
            self.db.query(GeneratedResume)
            .options(joinedload(GeneratedResume.components))
            .filter(GeneratedResume.uuid == resume_uuid)
            .first()
        )
    
    def get_user_resumes(self, user_id: int, skip: int = 0, limit: int = 100) -> List[GeneratedResume]:
        """Get all resumes for a user, ordered by creation date (most recent first)"""
        return (
            self.db.query(GeneratedResume)
            .options(joinedload(GeneratedResume.components))
            .filter(GeneratedResume.user_id == user_id)
            .order_by(GeneratedResume.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def update_resume(self, db_resume: GeneratedResume, resume_update: GeneratedResumeUpdate) -> GeneratedResume:
        """Update an existing resume"""
        update_data = resume_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_resume, field, value)
        
        self.db.commit()
        self.db.refresh(db_resume)
        return db_resume
    
    def delete_resume(self, db_resume: GeneratedResume) -> bool:
        """Delete a resume and its components"""
        self.db.delete(db_resume)
        self.db.commit()
        return True
    
    def create_component(self, resume_id: int, component_data: ResumeComponentCreate) -> ResumeComponent:
        """Create a new resume component"""
        db_component = ResumeComponent(
            resume_id=resume_id,
            **component_data.model_dump()
        )
        self.db.add(db_component)
        self.db.commit()
        self.db.refresh(db_component)
        return db_component
    
    def get_component_by_uuid(self, component_uuid: str) -> Optional[ResumeComponent]:
        """Get resume component by UUID"""
        return self.db.query(ResumeComponent).filter(ResumeComponent.uuid == component_uuid).first()
    
    def get_resume_components(self, resume_id: int) -> List[ResumeComponent]:
        """Get all components for a resume, ordered by order_index"""
        return (
            self.db.query(ResumeComponent)
            .filter(ResumeComponent.resume_id == resume_id)
            .order_by(ResumeComponent.order_index)
            .all()
        )
    
    def update_component(self, db_component: ResumeComponent, component_update: ResumeComponentUpdate) -> ResumeComponent:
        """Update an existing resume component"""
        update_data = component_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_component, field, value)
        
        self.db.commit()
        self.db.refresh(db_component)
        return db_component
    
    def delete_component(self, db_component: ResumeComponent) -> bool:
        """Delete a resume component"""
        self.db.delete(db_component)
        self.db.commit()
        return True
    
    def get_resume_by_job_title(self, user_id: int, job_title: str) -> Optional[GeneratedResume]:
        """Get resume by job title for a user"""
        return (
            self.db.query(GeneratedResume)
            .filter(GeneratedResume.user_id == user_id, GeneratedResume.job_title == job_title)
            .first()
        )
