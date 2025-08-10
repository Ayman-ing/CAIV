"""
Custom Section Router

FastAPI routes for custom section management.
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from core.dependencies import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.custom_sections.repository import CustomSectionRepository
from features.profiles.custom_sections.service import CustomSectionService
from features.profiles.custom_sections.schemas import CustomSectionCreate, CustomSectionUpdate, CustomSectionResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/custom-sections", tags=["custom-sections"])


def get_custom_section_service(db: Session = Depends(get_db)) -> CustomSectionService:
    """Dependency to get custom section service"""
    repository = CustomSectionRepository(db)
    return CustomSectionService(repository)


@router.post("/", response_model=CustomSectionResponse, status_code=201)
async def create_custom_section(
    section_data: CustomSectionCreate,
    current_user: User = Depends(get_current_user),
    service: CustomSectionService = Depends(get_custom_section_service)
):
    """Create a new custom section for the current user"""
    return service.create_section(current_user.id, section_data)


@router.get("/{section_uuid}", response_model=CustomSectionResponse)
async def get_custom_section(
    section_uuid: str,
    current_user: User = Depends(get_current_user),
    service: CustomSectionService = Depends(get_custom_section_service)
):
    """Get a specific custom section by UUID"""
    section = service.get_section_by_uuid(section_uuid)
    if not section:
        raise HTTPException(status_code=404, detail="Custom section not found")
    
    # Check ownership
    if not service.check_section_ownership(section_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this custom section")
    
    return section


@router.get("/user/{user_uuid}", response_model=List[CustomSectionResponse])
async def get_user_custom_sections(
    user_uuid: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    service: CustomSectionService = Depends(get_custom_section_service)
):
    """Get all custom sections for a specific user (UUID-based)"""
    # For now, users can only access their own custom sections
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, detail="Not authorized to access other users' custom sections")
    
    return service.get_user_sections(current_user.id, skip, limit)


@router.put("/{section_uuid}", response_model=CustomSectionResponse)
async def update_custom_section(
    section_uuid: str,
    section_update: CustomSectionUpdate,
    current_user: User = Depends(get_current_user),
    service: CustomSectionService = Depends(get_custom_section_service)
):
    """Update a custom section"""
    # Check ownership
    if not service.check_section_ownership(section_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this custom section")
    
    updated_section = service.update_section(section_uuid, section_update)
    if not updated_section:
        raise HTTPException(status_code=404, detail="Custom section not found")
    return updated_section


@router.delete("/{section_uuid}", status_code=204)
async def delete_custom_section(
    section_uuid: str,
    current_user: User = Depends(get_current_user),
    service: CustomSectionService = Depends(get_custom_section_service)
):
    """Delete a custom section"""
    # Check ownership
    if not service.check_section_ownership(section_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this custom section")
    
    success = service.delete_section(section_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Custom section not found")
