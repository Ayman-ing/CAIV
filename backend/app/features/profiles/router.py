"""
Profile Router

FastAPI routes for user profile management.
"""
import logging

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from core.exceptions import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.repository import ProfileRepository
from features.profiles.service import ProfileService
from features.profiles.schemas import ProfileCreate, ProfileUpdate, ProfileResponse
from features.vector_embeddings.tasks import index_profile_task

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/profiles", tags=["profiles"])


async def get_profile_service(db: AsyncSession = Depends(get_db)) -> ProfileService:
    """Dependency to get profile service"""
    repository = ProfileRepository(db)
    return ProfileService(repository)


@router.post("/", response_model=ProfileResponse, status_code=201)
async def create_profile(
    user_uuid: str,
    profile_data: ProfileCreate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Create a new profile for the specified user"""
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot create profile for another user")
    
    try:
        return await service.create_profile(current_user.id, profile_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.get("/", response_model=list[ProfileResponse])
async def get_user_profiles(
    user_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get all profiles for the specified user"""
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot access another user's profiles")
    
    profile = await service.get_user_profile(current_user.id)
    return [profile] if profile else []


@router.get("/{profile_uuid}", response_model=ProfileResponse)
async def get_profile(
    user_uuid: str,
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Get a specific profile for the user"""
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot access another user's profile")
    
    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot access another user's profile")
        
    profile = await service.get_profile_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")
    return profile


@router.put("/{profile_uuid}", response_model=ProfileResponse)
async def update_profile(
    user_uuid: str,
    profile_uuid: str,
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Update a specific profile"""
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot update another user's profile")
        
    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot update another user's profile")
    
    try:
        updated = await service.update_profile(profile_uuid, profile_data)
        if not updated:
            raise HTTPException(status_code=404, message="Profile not found")
        return updated
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))


@router.delete("/{profile_uuid}")
async def delete_profile(
    user_uuid: str,
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """Delete a specific profile"""
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot delete another user's profile")
        
    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot delete another user's profile")
    
    success = await service.delete_profile(profile_uuid)
    if not success:
        raise HTTPException(status_code=404, message="Profile not found")
    
    return {"message": "Profile deleted successfully"}


class IndexingResponse(BaseModel):
    """Response from profile indexing endpoint"""
    task_id: str
    message: str
    profile_uuid: str
    status: str


@router.post("/{profile_uuid}/index", response_model=IndexingResponse, status_code=202)
async def index_profile(
    user_uuid: str,
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    service: ProfileService = Depends(get_profile_service)
):
    """
    Trigger embedding generation and indexing for a profile.
    
    This endpoint starts an async task to generate embeddings for all profile items
    (work experiences, projects, skills, education, languages, certificates, etc.)
    and stores them in the vector database (pgvector).
    
    Returns a task ID that can be used to poll for status.
    """
    # Verify user owns this profile
    if str(current_user.uuid) != user_uuid:
        raise HTTPException(status_code=403, message="Cannot index another user's profile")
    
    if not await service.check_profile_ownership(profile_uuid, current_user.id):
        raise HTTPException(status_code=403, message="Cannot index another user's profile")
    
    # Verify profile exists
    profile = await service.get_profile_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")
    
    try:
        # Trigger async indexing task
        task = index_profile_task.delay(profile_uuid)
        
        logger.info(
            f"Indexing triggered for profile {profile_uuid} "
            f"(user {user_uuid}) → task_id={task.id}"
        )
        return IndexingResponse(
            task_id=task.id,
            message="Profile indexing started successfully",
            profile_uuid=profile_uuid,
            status="pending"
        )
    except Exception as e:
        logger.error(f"Failed to start indexing for profile {profile_uuid}: {str(e)}")
        raise HTTPException(status_code=500, message=f"Failed to start indexing: {str(e)}")
