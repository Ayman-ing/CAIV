"""
Profile Router

FastAPI routes for user profile management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.features.users.models import User
from app.features.profiles.repository import ProfileRepository
from app.features.profiles.service import ProfileService
from app.features.profiles.schemas import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    """Dependency to get profile service"""
    repository = ProfileRepository(db)
    return ProfileService(repository)


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Create a new profile for the current user"""
    try:
        return service.create_profile(current_user.id, profile_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/me", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get the current user's profile"""
    profile = service.get_user_profile(current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.get("/{profile_uuid}", response_model=ProfileResponse)
async def get_profile(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get a specific profile by UUID"""
    profile = service.get_profile_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Check ownership
    if not service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to access this profile")
    
    return profile


@router.put("/{profile_uuid}", response_model=ProfileResponse)
async def update_profile(
    profile_uuid: str,
    profile_update: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Update a profile"""
    # Check ownership
    if not service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to update this profile")
    
    updated_profile = service.update_profile(profile_uuid, profile_update)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated_profile


@router.delete("/{profile_uuid}", status_code=204)
async def delete_profile(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Delete a profile"""
    # Check ownership
    if not service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to delete this profile")
    
    success = service.delete_profile(profile_uuid)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
