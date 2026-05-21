from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from .models import Certificate
from .schemas import CertificateCreate, CertificateUpdate

class CertificateRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_with_profile_id(self, profile_id: int, certificate_data: CertificateCreate) -> Certificate:
        data_dict = certificate_data.model_dump()
        data_dict['profile_id'] = profile_id
        
        # Convert HttpUrl to string for database storage
        if data_dict.get('credential_url'):
            data_dict['credential_url'] = str(data_dict['credential_url'])
        
        certificate = Certificate(**data_dict)
        self.db.add(certificate)
        await self.db.commit()
        await self.db.refresh(certificate)
        return certificate
    
    async def get_by_uuid(self, certificate_uuid: str) -> Optional[Certificate]:
        result = await self.db.execute(select(Certificate).where(Certificate.uuid == certificate_uuid))
        return result.scalars().first()
    
    async def get_by_profile_id(self, profile_id: int, skip: int = 0, limit: int = 100) -> List[Certificate]:
        result = await self.db.execute(
            select(Certificate)
            .where(Certificate.profile_id == profile_id)
            .order_by(Certificate.issue_date.desc())
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()
    
    async def get_active_certificates(self, user_uuid: str) -> List[Certificate]:
        """Get non-expired certificates for a user"""
        from features.users.models import User
        from datetime import date
        
        today = date.today()
        result = await self.db.execute(
            select(Certificate)
            .join(User)
            .where(
                User.uuid == user_uuid,
                or_(
                    Certificate.expiration_date.is_(None),
                    Certificate.expiration_date >= today
                )
            )
            .order_by(Certificate.issue_date.desc())
        )
        return result.scalars().all()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Certificate]:
        result = await self.db.execute(select(Certificate).offset(skip).limit(limit))
        return result.scalars().all()
    
    async def update_by_uuid(self, certificate_uuid: str, certificate_data: CertificateUpdate) -> Optional[Certificate]:
        certificate = await self.get_by_uuid(certificate_uuid)
        if certificate:
            update_data = certificate_data.model_dump(exclude_unset=True)
            # Convert HttpUrl to string for database storage
            if update_data.get('credential_url'):
                update_data['credential_url'] = str(update_data['credential_url'])
            for field, value in update_data.items():
                setattr(certificate, field, value)
            await self.db.commit()
            await self.db.refresh(certificate)
        return certificate
    
    async def delete_by_uuid(self, certificate_uuid: str) -> bool:
        certificate = await self.get_by_uuid(certificate_uuid)
        if certificate:
            await self.db.delete(certificate)
            await self.db.commit()
            return True
        return False
