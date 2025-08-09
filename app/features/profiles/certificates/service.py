from sqlalchemy.orm import Session
from typing import Optional, List
from .repository import CertificateRepository
from .schemas import CertificateCreate, CertificateUpdate, CertificateResponse
from features.users.repository import UserRepository

class CertificateService:
    def __init__(self, db: Session):
        self.repository = CertificateRepository(db)
        self.user_repository = UserRepository(db)
    
    def create_certificate(self, certificate_data: CertificateCreate) -> CertificateResponse:
        user = self.user_repository.get_by_uuid(certificate_data.user_uuid)
        if not user:
            raise ValueError("User not found")
        
        certificate = self.repository.create_with_user_id(user.id, certificate_data)
        return CertificateResponse.model_validate(certificate)
    
    def get_certificate_by_uuid(self, certificate_uuid: str) -> Optional[CertificateResponse]:
        certificate = self.repository.get_by_uuid(certificate_uuid)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    def get_user_certificates_by_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[CertificateResponse]:
        certificates = self.repository.get_by_user_uuid(user_uuid, skip, limit)
        return [CertificateResponse.model_validate(c) for c in certificates]
    
    def get_user_active_certificates(self, user_uuid: str) -> List[CertificateResponse]:
        """Get only non-expired certificates for a user"""
        certificates = self.repository.get_active_certificates(user_uuid)
        return [CertificateResponse.model_validate(c) for c in certificates]
    
    def list_certificates(self, skip: int = 0, limit: int = 100) -> List[CertificateResponse]:
        certificates = self.repository.get_all(skip, limit)
        return [CertificateResponse.model_validate(c) for c in certificates]
    
    def update_certificate_by_uuid(self, certificate_uuid: str, certificate_data: CertificateUpdate) -> Optional[CertificateResponse]:
        certificate = self.repository.update_by_uuid(certificate_uuid, certificate_data)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    def delete_certificate_by_uuid(self, certificate_uuid: str) -> bool:
        return self.repository.delete_by_uuid(certificate_uuid)
