from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    location: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = True

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
