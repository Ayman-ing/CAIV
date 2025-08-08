from pydantic import BaseModel, HttpUrl
from datetime import datetime, date
from typing import Optional
import uuid

class CertificateBase(BaseModel):
    name: str
    issuer: str
    issue_date: date
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

class CertificateCreate(CertificateBase):
    user_uuid: str

class CertificateUpdate(BaseModel):
    name: Optional[str] = None
    issuer: Optional[str] = None
    issue_date: Optional[date] = None
    expiration_date: Optional[date] = None
    credential_id: Optional[str] = None
    credential_url: Optional[HttpUrl] = None

class CertificateResponse(CertificateBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
