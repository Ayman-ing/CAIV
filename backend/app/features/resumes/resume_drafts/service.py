from typing import List, Optional
from .repository import ResumeDraftRepository
from .schemas import ResumeDraftCreate, ResumeDraftUpdate, ResumeDraftResponse


class ResumeDraftService:

    def __init__(self, repository: ResumeDraftRepository):
        self.repository = repository

    async def create_draft(self, profile_id: int, data: ResumeDraftCreate) -> ResumeDraftResponse:
        draft = await self.repository.create(profile_id, data)
        return ResumeDraftResponse.model_validate(draft)

    async def get_draft(self, uuid: str) -> Optional[ResumeDraftResponse]:
        draft = await self.repository.get_by_uuid(uuid)
        if not draft:
            return None
        return ResumeDraftResponse.model_validate(draft)

    async def list_drafts(self, profile_id: int) -> List[ResumeDraftResponse]:
        drafts = await self.repository.list_by_profile(profile_id)
        return [ResumeDraftResponse.model_validate(d) for d in drafts]

    async def update_draft(self, uuid: str, data: ResumeDraftUpdate) -> Optional[ResumeDraftResponse]:
        draft = await self.repository.update(uuid, data)
        if not draft:
            return None
        return ResumeDraftResponse.model_validate(draft)

    async def delete_draft(self, uuid: str) -> bool:
        return await self.repository.delete(uuid)
