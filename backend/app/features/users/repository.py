from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid
from .models import User
from .schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_data: UserCreate) -> User:
        # Convert UserCreate to dict and remove password fields
        user_dict = user_data.model_dump()
        # Remove password fields as they should be handled by AuthService
        user_dict.pop('password', None)
        user_dict.pop('confirm_password', None)
        
        user = User(**user_dict)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_by_uuid(self, user_uuid: uuid.UUID) -> Optional[User]:
        """Get user by UUID object (repository layer always works with UUID objects)"""
        result = await self.db.execute(select(User).where(User.uuid == user_uuid))
        return result.scalars().first()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        result = await self.db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            await self.db.commit()
            await self.db.refresh(user)
        return user
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            await self.db.commit()
            return True
        return False
