from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid

from shared.models.base import Base


class ResumeDraft(Base):
    __tablename__ = 'resume_drafts'

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid.uuid4)
    profile_id = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    title = Column(String, nullable=False)
    template_name = Column(String, default='CANADIAN')
    draft_data = Column(JSONB, nullable=False, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    profile = relationship("Profile", foreign_keys=[profile_id])
