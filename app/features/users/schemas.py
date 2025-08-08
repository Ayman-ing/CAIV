from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
import uuid

class UserBase(BaseModel):
    email: EmailStr
    location: Optional[str] = None
    phone_number: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    uuid: uuid.UUID
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
