from sqlalchemy.orm import Session
from typing import Optional, List, Union
import uuid
from .repository import UserRepository
from .schemas import UserCreate, UserUpdate, UserResponse

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def _ensure_uuid(self, user_uuid: Union[str, uuid.UUID]) -> uuid.UUID:
        """Convert string UUID to UUID object if needed"""
        if isinstance(user_uuid, str):
            return uuid.UUID(user_uuid)
        return user_uuid
    
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user) if user else None
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """Alias for get_user for consistency with router"""
        return self.get_user(user_id)
    
    def get_user_by_uuid(self, user_uuid: Union[str, uuid.UUID]) -> Optional[UserResponse]:
        uuid_obj = self._ensure_uuid(user_uuid)
        user = self.repository.get_by_uuid(uuid_obj)
        return UserResponse.model_validate(user) if user else None
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        user = self.repository.get_by_email(email)
        return UserResponse.model_validate(user) if user else None
    
    def list_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_all(skip, limit)
        return [UserResponse.model_validate(user) for user in users]
    
    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        user = self.repository.update(user_id, user_data)
        return UserResponse.model_validate(user) if user else None
    
    def update_user_by_id(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """Alias for update_user for consistency with router"""
        return self.update_user(user_id, user_data)
    
    def update_user_by_uuid(self, user_uuid: Union[str, uuid.UUID], user_data: UserUpdate) -> Optional[UserResponse]:
        uuid_obj = self._ensure_uuid(user_uuid)
        user = self.repository.get_by_uuid(uuid_obj)
        if user:
            updated_user = self.repository.update(user.id, user_data)
            return UserResponse.model_validate(updated_user) if updated_user else None
        return None
    
    def delete_user_by_uuid(self, user_uuid: Union[str, uuid.UUID]) -> bool:
        uuid_obj = self._ensure_uuid(user_uuid)
        user = self.repository.get_by_uuid(uuid_obj)
        if user:
            return self.repository.delete(user.id)
        return False
    
    def delete_user_by_id(self, user_id: int) -> bool:
        """Delete user by ID"""
        return self.repository.delete(user_id)
