"""
Job Description Service

Business logic for job description management.
"""

from typing import List, Optional
from features.job_descriptions.repository import JobDescriptionRepository
from features.job_descriptions.schemas import JobDescriptionCreate, JobDescriptionUpdate, JobDescriptionResponse


class JobDescriptionService:
    """Service layer for job description business logic"""
    
    def __init__(self, repository: JobDescriptionRepository):
        self.repository = repository
    
    def create_job_description(self, user_id: int, job_desc_data: JobDescriptionCreate) -> JobDescriptionResponse:
        """Create a new job description"""
        # Check if user already has this URL
        existing_job_desc = self.repository.get_by_url(user_id, str(job_desc_data.url))
        if existing_job_desc:
            raise ValueError(f"Job description with URL '{job_desc_data.url}' already exists")
        
        db_job_desc = self.repository.create(user_id, job_desc_data)
        return JobDescriptionResponse.model_validate(db_job_desc)
    
    def get_job_description_by_uuid(self, job_desc_uuid: str) -> Optional[JobDescriptionResponse]:
        """Get job description by UUID"""
        db_job_desc = self.repository.get_by_uuid(job_desc_uuid)
        if not db_job_desc:
            return None
        return JobDescriptionResponse.model_validate(db_job_desc)
    
    def get_user_job_descriptions(self, user_id: int, skip: int = 0, limit: int = 100) -> List[JobDescriptionResponse]:
        """Get all job descriptions for a user"""
        db_job_descs = self.repository.get_user_job_descriptions(user_id, skip, limit)
        return [JobDescriptionResponse.model_validate(job_desc) for job_desc in db_job_descs]
    
    def update_job_description(self, job_desc_uuid: str, job_desc_update: JobDescriptionUpdate) -> Optional[JobDescriptionResponse]:
        """Update a job description"""
        db_job_desc = self.repository.get_by_uuid(job_desc_uuid)
        if not db_job_desc:
            return None
        
        # If updating URL, check for duplicates
        if job_desc_update.url:
            existing_job_desc = self.repository.get_by_url(db_job_desc.user_id, str(job_desc_update.url))
            if existing_job_desc and existing_job_desc.uuid != job_desc_uuid:
                raise ValueError(f"Job description with URL '{job_desc_update.url}' already exists")
        
        updated_job_desc = self.repository.update(db_job_desc, job_desc_update)
        return JobDescriptionResponse.model_validate(updated_job_desc)
    
    def delete_job_description(self, job_desc_uuid: str) -> bool:
        """Delete a job description"""
        db_job_desc = self.repository.get_by_uuid(job_desc_uuid)
        if not db_job_desc:
            return False
        
        return self.repository.delete(db_job_desc)
    
    def check_job_description_ownership(self, job_desc_uuid: str, user_id: int) -> bool:
        """Check if a job description belongs to a specific user"""
        db_job_desc = self.repository.get_by_uuid(job_desc_uuid)
        return db_job_desc is not None and db_job_desc.user_id == user_id
