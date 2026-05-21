from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .repository import CertificateRepository
from .schemas import CertificateCreate, CertificateUpdate, CertificateResponse
from features.profiles.repository import ProfileRepository

class CertificateService:
    def __init__(self, db: AsyncSession):
        self.repository = CertificateRepository(db)
        self.profile_repository = ProfileRepository(db)
    
    async def create_certificate(self, profile_uuid: str, certificate_data: CertificateCreate) -> CertificateResponse:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            raise ValueError("Profile not found")
        
        certificate = await self.repository.create_with_profile_id(profile.id, certificate_data)
        return CertificateResponse.model_validate(certificate)
    
    async def get_certificate_by_uuid(self, certificate_uuid: str) -> Optional[CertificateResponse]:
        certificate = await self.repository.get_by_uuid(certificate_uuid)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    async def get_certificates_by_profile(self, profile_uuid: str, skip: int = 0, limit: int = 100) -> List[CertificateResponse]:
        profile = await self.profile_repository.get_by_uuid(profile_uuid)
        if not profile:
            return []
        certificates = await self.repository.get_by_profile_id(profile.id, skip, limit)
        return [CertificateResponse.model_validate(c) for c in certificates]
    
    async def update_certificate_by_uuid(self, certificate_uuid: str, certificate_data: CertificateUpdate) -> Optional[CertificateResponse]:
        certificate = await self.repository.update_by_uuid(certificate_uuid, certificate_data)
        return CertificateResponse.model_validate(certificate) if certificate else None
    
    async def delete_certificate_by_uuid(self, certificate_uuid: str) -> bool:
        return await self.repository.delete_by_uuid(certificate_uuid)
