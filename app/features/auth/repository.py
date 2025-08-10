from sqlalchemy.orm import Session
from typing import Optional
import uuid
from features.users.models import User

class AuthRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email address"""
        return self.db.query(User).filter(User.email == email).first()
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_uuid(self, user_uuid: str) -> Optional[User]:
        """Get user by UUID"""
        # Convert string UUID to UUID object for SQLAlchemy
        try:
            uuid_obj = uuid.UUID(user_uuid)
            return self.db.query(User).filter(User.uuid == uuid_obj).first()
        except ValueError:
            # Invalid UUID format
            return None
    
    def create_user(self, email: str, password_hash: str, first_name: str = None, last_name: str = None) -> User:
        """Create a new user"""
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def update_user_password(self, user: User, new_password_hash: str) -> User:
        """Update user password"""
        user.password_hash = new_password_hash
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        return self.db.query(User).filter(User.email == email).first() is not None