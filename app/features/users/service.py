from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import UserRepository
from .schemas import UserCreate, UserUpdate, UserResponse

class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)
    
    def create_user(self, user_data: UserCreate) -> UserResponse:
        # Check if user already exists
        existing_user = self.repository.get_by_email(user_data.email)
        if existing_user:
            raise ValueError("User with this email already exists")
        
        user = self.repository.create(user_data)
        return UserResponse.model_validate(user)
    
    def get_user(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_by_id(user_id)
        return UserResponse.model_validate(user) if user else None
    
    def get_user_by_uuid(self, user_uuid: str) -> Optional[UserResponse]:
        user = self.repository.get_by_uuid(user_uuid)
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
    
    def update_user_by_uuid(self, user_uuid: str, user_data: UserUpdate) -> Optional[UserResponse]:
        user = self.repository.get_by_uuid(user_uuid)
        if user:
            updated_user = self.repository.update(user.id, user_data)
            return UserResponse.model_validate(updated_user) if updated_user else None
        return None
    
    def delete_user_by_uuid(self, user_uuid: str) -> bool:
        user = self.repository.get_by_uuid(user_uuid)
        if user:
            return self.repository.delete(user.id)
        return False
