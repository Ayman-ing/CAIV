from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from core.dependencies import get_db
from .service import CertificateService
from .schemas import CertificateCreate, CertificateUpdate, CertificateResponse

router = APIRouter(prefix="/api/v1/users/{user_id}/profiles/{profile_id}/certificates", tags=["certificates"])

@router.post("/", response_model=CertificateResponse, status_code=status.HTTP_201_CREATED)
def create_certificate(
    user_id: int,
    profile_id: int,
    certificate_data: CertificateCreate, 
    db: Session = Depends(get_db)
):
    """Create a new certificate for the specified profile"""
    service = CertificateService(db)
    try:
        return service.create_certificate(certificate_data, profile_id=profile_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{certificate_uuid}", response_model=CertificateResponse)
def get_certificate(certificate_uuid: str, db: Session = Depends(get_db)):
    """Get certificate by UUID"""
    service = CertificateService(db)
    certificate = service.get_certificate_by_uuid(certificate_uuid)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate

@router.get("/user/{user_uuid}", response_model=List[CertificateResponse])
def get_user_certificates(user_uuid: str, active_only: bool = False, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all certificates for a specific user by user UUID"""
    service = CertificateService(db)
    if active_only:
        return service.get_user_active_certificates(user_uuid)
    return service.get_user_certificates_by_uuid(user_uuid, skip, limit)

@router.get("/", response_model=List[CertificateResponse])
def list_certificates(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all certificates with pagination"""
    service = CertificateService(db)
    return service.list_certificates(skip, limit)

@router.put("/{certificate_uuid}", response_model=CertificateResponse)
def update_certificate(certificate_uuid: str, certificate_data: CertificateUpdate, db: Session = Depends(get_db)):
    """Update certificate information by UUID"""
    service = CertificateService(db)
    certificate = service.update_certificate_by_uuid(certificate_uuid, certificate_data)
    if not certificate:
        raise HTTPException(status_code=404, detail="Certificate not found")
    return certificate

@router.delete("/{certificate_uuid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_certificate(certificate_uuid: str, db: Session = Depends(get_db)):
    """Delete a certificate by UUID"""
    service = CertificateService(db)
    if not service.delete_certificate_by_uuid(certificate_uuid):
        raise HTTPException(status_code=404, detail="Certificate not found")
