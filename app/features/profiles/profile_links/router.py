"""
User Link Router

FastAPI routes for user link management.
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from core.exceptions import HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.profile_links.repository import ProfileLinkRepository
from features.profiles.profile_links.service import ProfileLinkService
from features.profiles.profile_links.schemas import ProfileLinkCreate, ProfileLinkUpdate, ProfileLinkResponse

router = APIRouter(prefix="/api/v1/profiles/{profile_id}/links", tags=["profile-links"])


def get_profile_link_service(db: Session = Depends(get_db)) -> ProfileLinkService:
    """Dependency to get user link service"""
    repository = ProfileLinkRepository(db)
    return ProfileLinkService(repository)


@router.post("/", response_model=ProfileLinkResponse, status_code=201)
async def create_user_link(
    link_data: ProfileLinkCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileLinkService = Depends(get_profile_link_service)
):
    """Create a new user link for the current user"""
    try:
        return service.create_link(current_user.id, link_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/{link_uuid}", response_model=ProfileLinkResponse)
async def get_user_link(
    link_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileLinkService = Depends(get_profile_link_service)
):
    """Get a specific user link by UUID"""
    link = service.get_link_by_uuid(link_uuid)
    if not link:
        raise HTTPException(status_code=404, message="User link not found")
    
    # Check ownership
    if not service.check_link_ownership(link_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to access this link")
    
    return link


@router.get("/user/{user_uuid}", response_model=List[ProfileLinkResponse])
async def get_profile_links(
    user_uuid: str,
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(100, ge=1, le=1000, description="Maximum number of records to return"),
    current_user: User = Depends(get_current_user),
    service: ProfileLinkService = Depends(get_profile_link_service)
):
    """Get all links for a specific user (UUID-based)"""
    # For now, users can only access their own links
    if user_uuid != current_user.uuid:
        raise HTTPException(status_code=403, message="Not authorized to access other users' links")
    
    return service.get_profile_links(current_user.id, skip, limit)


@router.put("/{link_uuid}", response_model=ProfileLinkResponse)
async def update_profile_link(
    link_uuid: str,
    link_update: ProfileLinkUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileLinkService = Depends(get_profile_link_service)
):
    """Update a user link"""
    # Check ownership
    if not service.check_link_ownership(link_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to update this link")
    
    try:
        updated_link = service.update_link(link_uuid, link_update)
        if not updated_link:
            raise HTTPException(status_code=404, message="User link not found")
        return updated_link
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.delete("/{link_uuid}", status_code=204)
async def delete_user_link(
    link_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileLinkService = Depends(get_profile_link_service)
):
    """Delete a user link"""
    # Check ownership
    if not service.check_link_ownership(link_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Not authorized to delete this link")
    
    success = service.delete_link(link_uuid)
    if not success:
        raise HTTPException(status_code=404, message="User link not found")
