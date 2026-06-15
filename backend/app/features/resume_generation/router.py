import logging
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.session import get_db
from core.exceptions import HTTPException
from features.auth.dependencies import get_current_user
from features.users.models import User
from features.profiles.repository import ProfileRepository
from features.resume_generation.service import ResumeGenerationService
from features.resume_generation.schemas import GenerateRequest, GenerateResponse

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/profiles/{profile_uuid}/generate-resume",
    tags=["resume-generation"],
)


@router.post("/", response_model=GenerateResponse, status_code=status.HTTP_201_CREATED)
async def generate_resume(
    profile_uuid: str,
    request: GenerateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    profile_repo = ProfileRepository(db)
    profile = await profile_repo.get_by_uuid(profile_uuid)
    if not profile:
        raise HTTPException(status_code=404, message="Profile not found")
    if profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Access denied to this profile")

    service = ResumeGenerationService(db)
    try:
        return await service.generate(profile_uuid, request, current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))
    except Exception as e:
        logger.error(f"Resume generation failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, message=f"Resume generation failed: {str(e)}")
