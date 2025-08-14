from sqlalchemy.orm import Session
from typing import Optional, List
import uuid
from .models import User
from .schemas import UserCreate, UserUpdate

class UserRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, user_data: UserCreate) -> User:
        # Convert UserCreate to dict and remove password fields
        user_dict = user_data.model_dump()
        # Remove password fields as they should be handled by AuthService
        user_dict.pop('password', None)
        user_dict.pop('confirm_password', None)
        
        user = User(**user_dict)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_by_uuid(self, user_uuid: uuid.UUID) -> Optional[User]:
        """Get user by UUID object (repository layer always works with UUID objects)"""
        return self.db.query(User).filter(User.uuid == user_uuid).first()
    
    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        return self.db.query(User).offset(skip).limit(limit).all()
    
    def update(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        user = self.get_by_id(user_id)
        if user:
            for field, value in user_data.model_dump(exclude_unset=True).items():
                setattr(user, field, value)
            self.db.commit()
            self.db.refresh(user)
        return user
    
    def delete(self, user_id: int) -> bool:
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
            return True
        return False
