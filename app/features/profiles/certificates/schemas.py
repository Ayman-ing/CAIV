from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime, date
from typing import Optional
import uuid

class CertificateBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Certificate name")
    issuer: str = Field(..., min_length=1, max_length=200, description="Issuing organization")
    issue_date: date = Field(..., description="Date certificate was issued")
    expiration_date: Optional[date] = Field(None, description="Certificate expiration date (None if no expiration)")
    credential_id: Optional[str] = Field(None, max_length=100, description="Credential ID or license number")
    credential_url: Optional[HttpUrl] = Field(None, description="URL to verify the certificate")
    
    @validator('expiration_date')
    def validate_expiration_date(cls, v, values):
        if v is not None and 'issue_date' in values and v < values['issue_date']:
            raise ValueError('Expiration date must be after issue date')
        return v

class CertificateCreate(CertificateBase):
    """Schema for creating certificate - profile_id comes from URL path"""
    pass

class CertificateUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    issuer: Optional[str] = Field(None, min_length=1, max_length=200)
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = Field(None, max_length=100)
    credential_url: Optional[HttpUrl] = None
    
    @validator('expiration_date')
    def validate_expiration_date(cls, v, values):
        if v is not None and 'issue_date' in values and v < values['issue_date']:
            raise ValueError('Expiration date must be after issue date')
        return v

class CertificateResponse(CertificateBase):
    uuid: uuid.UUID
    profile_id: int = Field(..., description="Profile this certificate belongs to")
    user_id: int = Field(..., description="User who owns this certificate")
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
