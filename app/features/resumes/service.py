"""
Resume Service

Business logic for resume and component management.
"""

from typing import List, Optional
from .repository import ResumeRepository
from .schemas import (
    GeneratedResumeCreate, GeneratedResumeUpdate, GeneratedResumeResponse,
    ResumeComponentCreate, ResumeComponentUpdate, ResumeComponentResponse
)
from .models import GeneratedResume, ResumeComponent


class ResumeService:
    """Service layer for resume business logic"""
    
    def __init__(self, repository: ResumeRepository):
        self.repository = repository
    
    def create_resume(self, user_id: int, resume_data: GeneratedResumeCreate) -> GeneratedResumeResponse:
        """Create a new resume"""
        # Check if user already has a resume for this job title
        existing_resume = self.repository.get_resume_by_job_title(
            user_id=user_id, 
            job_title=resume_data.job_title
        )
        
        if existing_resume:
            raise ValueError(f"Resume for job title '{resume_data.job_title}' already exists")
        
        db_resume = self.repository.create_resume(user_id, resume_data)
        return GeneratedResumeResponse.model_validate(db_resume)
    
    def get_resume_by_uuid(self, resume_uuid: str) -> Optional[GeneratedResumeResponse]:
        """Get resume by UUID with all components"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        if not db_resume:
            return None
        return GeneratedResumeResponse.model_validate(db_resume)
    
    def get_user_resumes(self, user_id: int, skip: int = 0, limit: int = 100) -> List[GeneratedResumeResponse]:
        """Get all resumes for a user"""
        db_resumes = self.repository.get_user_resumes(user_id, skip, limit)
        return [GeneratedResumeResponse.model_validate(resume) for resume in db_resumes]
    
    def update_resume(self, resume_uuid: str, resume_update: GeneratedResumeUpdate) -> Optional[GeneratedResumeResponse]:
        """Update a resume"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        if not db_resume:
            return None
        
        # If updating job title, check for duplicates
        if resume_update.job_title:
            existing_resume = self.repository.get_resume_by_job_title(
                user_id=db_resume.user_id,
                job_title=resume_update.job_title
            )
            if existing_resume and existing_resume.uuid != resume_uuid:
                raise ValueError(f"Resume for job title '{resume_update.job_title}' already exists")
        
        updated_resume = self.repository.update_resume(db_resume, resume_update)
        return GeneratedResumeResponse.model_validate(updated_resume)
    
    def delete_resume(self, resume_uuid: str) -> bool:
        """Delete a resume and all its components"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        if not db_resume:
            return False
        
        return self.repository.delete_resume(db_resume)
    
    def create_component(self, resume_uuid: str, component_data: ResumeComponentCreate) -> Optional[ResumeComponentResponse]:
        """Create a new resume component"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        if not db_resume:
            return None
        
        db_component = self.repository.create_component(db_resume.id, component_data)
        return ResumeComponentResponse.model_validate(db_component)
    
    def get_component_by_uuid(self, component_uuid: str) -> Optional[ResumeComponentResponse]:
        """Get component by UUID"""
        db_component = self.repository.get_component_by_uuid(component_uuid)
        if not db_component:
            return None
        return ResumeComponentResponse.model_validate(db_component)
    
    def get_resume_components(self, resume_uuid: str) -> Optional[List[ResumeComponentResponse]]:
        """Get all components for a resume"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        if not db_resume:
            return None
        
        db_components = self.repository.get_resume_components(db_resume.id)
        return [ResumeComponentResponse.model_validate(comp) for comp in db_components]
    
    def update_component(self, component_uuid: str, component_update: ResumeComponentUpdate) -> Optional[ResumeComponentResponse]:
        """Update a resume component"""
        db_component = self.repository.get_component_by_uuid(component_uuid)
        if not db_component:
            return None
        
        updated_component = self.repository.update_component(db_component, component_update)
        return ResumeComponentResponse.model_validate(updated_component)
    
    def delete_component(self, component_uuid: str) -> bool:
        """Delete a resume component"""
        db_component = self.repository.get_component_by_uuid(component_uuid)
        if not db_component:
            return False
        
        return self.repository.delete_component(db_component)
    
    def check_resume_ownership(self, resume_uuid: str, user_id: int) -> bool:
        """Check if a resume belongs to a specific user"""
        db_resume = self.repository.get_resume_by_uuid(resume_uuid)
        return db_resume is not None and db_resume.user_id == user_id
    
    def check_component_ownership(self, component_uuid: str, user_id: int) -> bool:
        """Check if a component belongs to a specific user (through resume)"""
        db_component = self.repository.get_component_by_uuid(component_uuid)
        if not db_component:
            return False
        
        db_resume = self.repository.get_resume_by_uuid(db_component.resume.uuid)
        return db_resume is not None and db_resume.user_id == user_id
