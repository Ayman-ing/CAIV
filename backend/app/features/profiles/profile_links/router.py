from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import ProfileLinkService
from .schemas import ProfileLinkCreate, ProfileLinkUpdate, ProfileLinkResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/links", tags=["profile-links"])

async def check_profile_ownership(db: AsyncSession, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = await repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's links")
    return profile

@router.post("/", response_model=ProfileLinkResponse, status_code=status.HTTP_201_CREATED)
async def create_link(
    profile_uuid: str,
    link_data: ProfileLinkCreate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new link for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProfileLinkService(db)
    try:
        return await service.create_link(profile_uuid, link_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[ProfileLinkResponse])
async def get_profile_links(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all links for the specified profile"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProfileLinkService(db)
    return await service.get_links_by_profile(profile_uuid)

@router.put("/{link_uuid}", response_model=ProfileLinkResponse)
async def update_link(
    profile_uuid: str,
    link_uuid: str, 
    link_data: ProfileLinkUpdate, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update link information by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProfileLinkService(db)
    link = await service.update_link_by_uuid(link_uuid, link_data)
    if not link:
        raise HTTPException(status_code=404, message="Link not found")
    return link

@router.delete("/{link_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_link(
    profile_uuid: str,
    link_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a link by UUID"""
    await check_profile_ownership(db, current_user, profile_uuid)
    service = ProfileLinkService(db)
    if not await service.delete_link_by_uuid(link_uuid):
        raise HTTPException(status_code=404, message="Link not found")
