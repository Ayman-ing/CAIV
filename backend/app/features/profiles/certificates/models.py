from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.entity import BaseEntity

class Certificate(BaseEntity):
    __tablename__ = 'certificates'
    
    # Primary key that's also a foreign key to the parent entities table
    id = Column(Integer, ForeignKey('entities.id'), primary_key=True)
    
    # Certificate specific fields
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    name = Column(String)
    issuer = Column(String)
    issue_date = Column(Date)
    expiration_date = Column(Date)
    credential_id = Column(String)
    credential_url = Column(String)
    
    # Relationships
    profile = relationship("Profile", back_populates="certificates")
    # embeddings relationship is inherited from BaseEntity via Entity table
    
    __mapper_args__ = {
        'polymorphic_identity': 'certificate',
    }
    
    __mapper_args__ = {
        'polymorphic_identity': 'certificate',
    }
