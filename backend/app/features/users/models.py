from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum

from shared.models.base import Base

class UserRole(enum.Enum):
    """User roles for RBAC"""
    USER = "user"
    ADMIN = "admin"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    password_hash = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, index=True)
    first_name = Column(String, nullable=False)  # Now required
    last_name = Column(String, nullable=False)   # Now required
    
    # Role and status
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime)
    
    # Relationships - 1-to-1 with Profile
    profile = relationship("Profile", back_populates="user", uselist=False)
    job_descriptions = relationship("JobDescription", back_populates="user")
    
    @property
    def is_admin(self) -> bool:
        """Check if user has admin role"""
        return self.role == UserRole.ADMIN
    
    @property
    def full_name(self) -> str:
        """Get user's full name"""
        return f"{self.first_name} {self.last_name}"
    
    def has_permission(self, permission: str) -> bool:
        """Check if user has specific permission"""
        admin_permissions = [
            "manage_users", "view_all_profiles", "view_all_resumes", 
            "delete_any_user", "view_analytics", "manage_system_settings",
            "access_admin_panel"
        ]
        
        user_permissions = [
            "create_profile", "read_own_profile", "update_own_profile", "delete_own_profile",
            "create_resume", "read_own_resume", "update_own_resume", "delete_own_resume",
            "change_password", "update_account"
        ]
        
        if self.role == UserRole.ADMIN:
            return permission in admin_permissions or permission in user_permissions
        else:
            return permission in user_permissions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    
    profiles = relationship("Profile", back_populates="user")
    job_descriptions = relationship("JobDescription", back_populates="user")