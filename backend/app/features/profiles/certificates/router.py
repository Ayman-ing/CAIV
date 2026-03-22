from fastapi import APIRouter, Depends, status
from core.exceptions import HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from features.auth.dependencies import get_current_user
from features.users.models import User
from .service import CertificateService
from .schemas import CertificateCreate, CertificateUpdate, CertificateResponse
from features.profiles.repository import ProfileRepository

router = APIRouter(prefix="/api/v1/profiles/{profile_uuid}/certificates", tags=["certificates"])

def check_profile_ownership(db: Session, current_user: User, profile_uuid: str):
    """Ensure the user owns the profile they are trying to manipulate"""
    repo = ProfileRepository(db)
    profile = repo.get_by_uuid(profile_uuid)
    if not profile or profile.user_id != current_user.id:
        raise HTTPException(status_code=403, message="Not authorized to access this profile's certificates")
    return profile

@router.post("/", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
def create_certificate(
    profile_uuid: str,
    certificate_data: CertificateCreate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new certificate for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CertificateService(db)
    try:
        return service.create_certificate(profile_uuid, certificate_data)
    except ValueError as e:
        raise HTTPException(status_code=400, message=str(e))

@router.get("/", response_model=List[CertificateResponse])
def get_profile_certificates(
    profile_uuid: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all certificates for the specified profile"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CertificateService(db)
    return service.get_certificates_by_profile(profile_uuid)

@router.put("/{certificate_uuid}", response_model=CertificateResponse)
def update_certificate(
    profile_uuid: str,
    certificate_uuid: str, 
    certificate_data: CertificateUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update certificate information by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CertificateService(db)
    certificate = service.update_certificate_by_uuid(certificate_uuid, certificate_data)
    if not certificate:
        raise HTTPException(status_code=404, message="Certificate not found")
    return certificate

@router.delete("/{certificate_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(
    profile_uuid: str,
    certificate_uuid: str, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a certificate by UUID"""
    check_profile_ownership(db, current_user, profile_uuid)
    service = CertificateService(db)
    if not service.delete_certificate_by_uuid(certificate_uuid):
        raise HTTPException(status_code=404, message="Certificate not found")
