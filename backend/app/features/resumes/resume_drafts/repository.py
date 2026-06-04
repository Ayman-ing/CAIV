from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .models import ResumeDraft
from .schemas import ResumeDraftCreate, ResumeDraftUpdate


class ResumeDraftRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, profile_id: int, data: ResumeDraftCreate) -> ResumeDraft:
        draft = ResumeDraft(
            profile_id=profile_id,
            title=data.title,
            template_name=data.template_name,
            draft_data=data.draft_data,
        )
        self.db.add(draft)
        await self.db.commit()
        await self.db.refresh(draft)
        return draft

    async def get_by_uuid(self, uuid: str) -> Optional[ResumeDraft]:
        result = await self.db.execute(
            select(ResumeDraft).where(ResumeDraft.uuid == uuid)
        )
        return result.scalars().first()

    async def list_by_profile(self, profile_id: int) -> List[ResumeDraft]:
        result = await self.db.execute(
            select(ResumeDraft)
            .where(ResumeDraft.profile_id == profile_id)
            .order_by(ResumeDraft.updated_at.desc())
        )
        return result.scalars().all()

    async def update(self, uuid: str, data: ResumeDraftUpdate) -> Optional[ResumeDraft]:
        draft = await self.get_by_uuid(uuid)
        if not draft:
            return None
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(draft, field, value)
        await self.db.commit()
        await self.db.refresh(draft)
        return draft

    async def delete(self, uuid: str) -> bool:
        draft = await self.get_by_uuid(uuid)
        if not draft:
            return False
        await self.db.delete(draft)
        await self.db.commit()
        return True
