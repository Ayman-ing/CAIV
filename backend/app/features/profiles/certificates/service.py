from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import CertificateRepository
from .schemas import CertificateCreate, CertificateUpdate, CertificateResponse
from features.profiles.repository import ProfileRepository

class CertificateService:
    def __init__(self, db: Session):
        self.repository = CertificateRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    def create_certificate(self, profile_uuid: str, certificate_data: CertificateCreate) -> CertificateResponse:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        certificate = self.repository.create_with_profile_id(profile.id, certificate_data)
        return CertificateResponse.model_validate(certificate)
    
    def get_certificate_by_uuid(self, certificate_uuid: str) -> Optional[CertificateResponse]:
        certificate = self.repository.get_by_uuid(certificate_uuid)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    def get_certificates_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[CertificateResponse]:
        profile = self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        certificates = self.repository.get_by_profile_id(profile.id, skip, limit)
        return [CertificateResponse.model_validate(c) for c in certificates]
    
    def update_certificate_by_uuid(self, certificate_uuid: str, certificate_data: CertificateUpdate) -> Optional[CertificateResponse]:
        certificate = self.repository.update_by_uuid(certificate_uuid, certificate_data)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    def delete_certificate_by_uuid(self, certificate_uuid: str) -> bool:
        return self.repository.delete_by_uuid(certificate_uuid)
