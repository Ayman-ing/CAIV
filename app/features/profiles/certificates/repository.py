from sqlalchemy.orm import Session
from typing import Optional, List
from .models import Certificate
from .schemas import CertificateCreate, CertificateUpdate

class CertificateRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_with_user_id(self, user_id: int, certificate_data: CertificateCreate) -> Certificate:
        data_dict = certificate_data.model_dump()
        data_dict.pop('user_uuid', None)
        data_dict['user_id'] = user_id
        
        certificate = Certificate(**data_dict)
        self.db.add(certificate)
        self.db.commit()
        self.db.refresh(certificate)
        return certificate
    
    def get_by_uuid(self, certificate_uuid: str) -> Optional[Certificate]:
        return self.db.query(Certificate).filter(Certificate.uuid == certificate_uuid).first()
    
    def get_by_user_uuid(self, user_uuid: str, skip: int = 0, limit: int = 100) -> List[Certificate]:
        from features.users.models import User
        return (self.db.query(Certificate)
                .join(User)
                .filter(User.uuid == user_uuid)
                .order_by(Certificate.issue_date.desc())
                .offset(skip)
                .limit(limit)
                .all())
    
    def get_active_certificates(self, user_uuid: str) -> List[Certificate]:
        """Get non-expired certificates for a user"""
        from features.users.models import User
        from sqlalchemy import or_
        from datetime import date
        
        today = date.today()
        return (self.db.query(Certificate)
                .join(User)
                .filter(
                    User.uuid == user_uuid,
                    or_(
                        Certificate.expiration_date.is_(None),
                        Certificate.expiration_date >= today
                    )
                )
                .order_by(Certificate.issue_date.desc())
                .all())
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Certificate]:
        return self.db.query(Certificate).offset(skip).limit(limit).all()
    
    def update_by_uuid(self, certificate_uuid: str, certificate_data: CertificateUpdate) -> Optional[Certificate]:
        certificate = self.get_by_uuid(certificate_uuid)
        if certificate:
            for field, value in certificate_data.model_dump(exclude_unset=True).items():
                setattr(certificate, field, value)
            self.db.commit()
            self.db.refresh(certificate)
        return certificate
    
    def delete_by_uuid(self, certificate_uuid: str) -> bool:
        certificate = self.get_by_uuid(certificate_uuid)
        if certificate:
            self.db.delete(certificate)
            self.db.commit()
            return True
        return False
