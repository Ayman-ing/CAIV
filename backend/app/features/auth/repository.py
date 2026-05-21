from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import uuid
from features.users.models import User, UserRole

class AuthRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by UUID"""
        # Convert string UUID to UUID object for SQLAlchemy
        try:
            uuid_obj = uuid.UUID(user_uuid)
            result = await self.db.execute(select(User).where(User.uuid == uuid_obj))
            return result.scalars().first()
        except ValueError:
            # Invalid UUID format
            return None
    
    async def create_user(self, email: str, password_hash: str, first_name: str = None, last_name: str = None,role : str = UserRole.USER) -> User:
        """Create a new user"""
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role
        )
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def update_user_password(self, user: User, new_password_hash: str) -> User:
        """Update user password"""
        user.password_hash = new_password_hash
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first() is not None