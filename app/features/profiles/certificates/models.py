from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declared_attr
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Certificate(BaseEntity):
    __tablename__ = 'certificates'
    
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    name = Column(String)
    issuer = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    credential_id = Column(String)
    credential_url = Column(String)
    
    @declared_attr
    def profile(cls):
        return relationship("Profile", back_populates="certificates")
    # embeddings relationship is inherited from BaseEntity
