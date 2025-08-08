"""
Job Description Repository

Handles all database operations for job descriptions.
"""

from typing import List, Optional
from sqlalchemy.orm import Session
from .models import JobDescription
from .schemas import JobDescriptionCreate, JobDescriptionUpdate


class JobDescriptionRepository:
    """Repository for job description database operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_id: int, job_desc_data: JobDescriptionCreate) -> JobDescription:
        """Create a new job description"""
        db_job_desc = JobDescription(
            user_id=user_id,
            url=str(job_desc_data.url)
        )
        self.db.add(db_job_desc)
        self.db.commit()
        self.db.refresh(db_job_desc)
        return db_job_desc
    
    def get_by_uuid(self, job_desc_uuid: str) -> Optional[JobDescription]:
        """Get job description by UUID"""
        return self.db.query(JobDescription).filter(JobDescription.uuid == job_desc_uuid).first()
    
    def get_user_job_descriptions(self, user_id: int, skip: int = 0, limit: int = 100) -> List[JobDescription]:
        """Get all job descriptions for a user, ordered by creation date (most recent first)"""
        return (
            self.db.query(JobDescription)
            .filter(JobDescription.user_id == user_id)
            .order_by(JobDescription.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
    
    def get_by_url(self, user_id: int, url: str) -> Optional[JobDescription]:
        """Get job description by URL for a specific user"""
        return (
            self.db.query(JobDescription)
            .filter(JobDescription.user_id == user_id, JobDescription.url == url)
            .first()
        )
    
    def update(self, db_job_desc: JobDescription, job_desc_update: JobDescriptionUpdate) -> JobDescription:
        """Update an existing job description"""
        update_data = job_desc_update.model_dump(exclude_unset=True)
        
        # Convert URL to string if provided
        if 'url' in update_data and update_data['url'] is not None:
            update_data['url'] = str(update_data['url'])
        
        for field, value in update_data.items():
            setattr(db_job_desc, field, value)
        
        self.db.commit()
        self.db.refresh(db_job_desc)
        return db_job_desc
    
    def delete(self, db_job_desc: JobDescription) -> bool:
        """Delete a job description"""
        self.db.delete(db_job_desc)
        self.db.commit()
        return True
