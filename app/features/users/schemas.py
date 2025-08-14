from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid
from .models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name (required)")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name (required)")
    is_active: Optional[bool] = True
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if not v or not v.strip():
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip()

class UserCreate(UserBase):
    password: str
    confirm_password: str
    role : str = UserRole.USER.value  # Default to USER role
    

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    first_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, min_length=1, max_length=50, description="User's last name")
    is_active: Optional[bool] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    role: Optional[UserRole] = None
    
    @field_validator('first_name', 'last_name')
    @classmethod
    def validate_names(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Name cannot be empty or just whitespace')
        return v.strip() if v else v

class UserResponse(UserBase):
    id: int
    uuid: uuid.UUID
    role: UserRole
    is_verified: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
