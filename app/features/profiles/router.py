"""
Profile Router

FastAPI routes for user profile management.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.repository import ProfileRepository
from features.profiles.service import ProfileService
from features.profiles.schemas import ProfileCreate, ProfileUpdate, ProfileResponse

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


def get_profile_service(db: Session = Depends(get_db)) -> ProfileService:
    """Dependency to get profile service"""
    repository = ProfileRepository(db)
    return ProfileService(repository)


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
    user_id: int,
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Create a new profile for the specified user"""
    # Ensure user can only create profiles for themselves (or add admin check later)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot create profile for another user")
    
    try:
        return service.create_profile(user_id, profile_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=list[ProfileResponse])
async def get_user_profiles(
    user_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get all profiles for the specified user"""
    # Ensure user can only access their own profiles (or add admin check later)
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's profiles")
    
    return service.get_user_profiles(user_id)


@router.get("/{profile_id}", response_model=ProfileResponse)
async def get_profile(
    user_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get a specific profile for the user"""
    # Ensure user can only access their own profiles
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot access another user's profile")
    
    profile = service.get_profile(profile_id, user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/{profile_id}", response_model=ProfileResponse)
async def update_profile(
    user_id: int,
    profile_id: int,
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Update a specific profile"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot update another user's profile")
    
    try:
        return service.update_profile(profile_id, user_id, profile_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/{profile_id}")
async def delete_profile(
    user_id: int,
    profile_id: int,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Delete a specific profile"""
    # Check ownership
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Cannot delete another user's profile")
    
    success = service.delete_profile(profile_id, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    return {"message": "Profile deleted successfully"}
