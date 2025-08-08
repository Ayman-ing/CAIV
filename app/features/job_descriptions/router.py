"""
Job Description Router

FastAPI routes for job description management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.features.users.models import User
from app.features.job_descriptions.repository import JobDescriptionRepository
from app.features.job_descriptions.service import JobDescriptionService
from app.features.job_descriptions.schemas import JobDescriptionCreate, JobDescriptionUpdate, JobDescriptionResponse

router = APIRouter(prefix="/api/v1/job-descriptions", tags=["job-descriptions"])


def get_job_description_service(db: Session = Depends(get_db)) -> JobDescriptionService:
    """Dependency to get job description service"""
    repository = JobDescriptionRepository(db)
    return JobDescriptionService(repository)


@router.post("/", response_model=JobDescriptionResponse, status_code=201)
async def create_job_description(
    job_desc_data: JobDescriptionCreate,
    current_user: User = Depends(get_current_user),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Create a new job description for the current user"""
    try:
        return service.create_job_description(current_user.id, job_desc_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{job_desc_uuid}", response_model=JobDescriptionResponse)
async def get_job_description(
    job_desc_uuid: str,
    current_user: User = Depends(get_current_user),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Get a specific job description by UUID"""
    job_desc = service.get_job_description_by_uuid(job_desc_uuid)
    if not job_desc:
        raise HTTPException(status_code=404, detail="Job description not found")
    
    # Check ownership
    if not service.check_job_description_ownership(job_desc_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this job description")
    
    return job_desc


@router.get("/user/{user_uuid}", response_model=List[JobDescriptionResponse])
async def get_user_job_descriptions(
    user_uuid: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Get all job descriptions for a specific user (UUID-based)"""
    # For now, users can only access their own job descriptions
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not authorized to access other users' job descriptions")
    
    return service.get_user_job_descriptions(current_user.id, skip, limit)


@router.put("/{job_desc_uuid}", response_model=JobDescriptionResponse)
async def update_job_description(
    job_desc_uuid: str,
    job_desc_update: JobDescriptionUpdate,
    current_user: User = Depends(get_current_user),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Update a job description"""
    # Check ownership
    if not service.check_job_description_ownership(job_desc_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this job description")
    
    try:
        updated_job_desc = service.update_job_description(job_desc_uuid, job_desc_update)
        if not updated_job_desc:
            raise HTTPException(status_code=404, detail="Job description not found")
        return updated_job_desc
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{job_desc_uuid}", status_code=204)
async def delete_job_description(
    job_desc_uuid: str,
    current_user: User = Depends(get_current_user),
    service: JobDescriptionService = Depends(get_job_description_service)
):
    """Delete a job description"""
    # Check ownership
    if not service.check_job_description_ownership(job_desc_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this job description")
    
    success = service.delete_job_description(job_desc_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Job description not found")
