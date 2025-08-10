from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator
from typing import Optional
from uuid import UUID

class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, description="User's password")

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "user@example.com",
                "password": "secretpassword"
            }
        }
    }

class UserRegister(BaseModel):
    """Schema for user registration"""
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=6, max_length=100, description="User's password")
    confirm_password: str = Field(..., min_length=6, max_length=100, description="Password confirmation")
    first_name: Optional[str] = Field(None, max_length=50, description="User's first name")
    last_name: Optional[str] = Field(None, max_length=50, description="User's last name")
    
    @model_validator(mode='after')
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "email": "newuser@example.com",
                "password": "secretpassword",
                "confirm_password": "secretpassword"
            }
        }
    }

class Token(BaseModel):
    """Schema for JWT token response"""
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Token expiration time in seconds")
    user_id: UUID = Field(..., description="Authenticated user ID")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 1800,
                "user_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }

class TokenData(BaseModel):
    """Schema for token data validation"""
    user_id: Optional[UUID] = None
    email: Optional[str] = None

class PasswordChange(BaseModel):
    """Schema for changing password"""
    current_password: str = Field(..., min_length=6, description="Current password")
    new_password: str = Field(..., min_length=6, max_length=100, description="New password")
    confirm_new_password: str = Field(..., min_length=6, max_length=100, description="New password confirmation")
    
    @model_validator(mode='after')
    def new_passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError('New passwords do not match')
        return self

class PasswordReset(BaseModel):
    """Schema for password reset request"""
    email: EmailStr = Field(..., description="Email address for password reset")

class PasswordResetConfirm(BaseModel):
    """Schema for password reset confirmation"""
    token: str = Field(..., description="Password reset token")
    new_password: str = Field(..., min_length=6, max_length=100, description="New password")
    confirm_new_password: str = Field(..., min_length=6, max_length=100, description="New password confirmation")
    
    @model_validator(mode='after')
    def passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError('Passwords do not match')
        return self