from pydantic import BaseModel, EmailStr, Field, field_validator
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: EmailStr
    first_name: str = Field(..., min_length=1, max_length=50, description="User's first name (required)")
    last_name: str = Field(..., min_length=1, max_length=50, description="User's last name (required)")
    location: Optional[str] = None
    phone_number: Optional[str] = None
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
    

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
