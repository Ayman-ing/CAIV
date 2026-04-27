"""
Resume Import Models - Track uploaded CVs and extracted data
"""
import uuid as uuid_lib
from datetime import datetime
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from shared.models.base import Base


class UploadedResume(Base):
    """Track uploaded PDF CVs and their extraction status"""

    __tablename__ = "uploaded_resumes"

    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), unique=True, default=uuid_lib.uuid4, nullable=False)

    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    original_filename = Column(String(255), nullable=False)
    extracted_data = Column(JSON, nullable=False)  # Full extracted data from PDF

    import_status = Column(
        String(50),
        default="pending",
        nullable=False,
    )  # pending, confirmed, rejected

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    profile = relationship("Profile", back_populates="uploaded_resumes")
    user = relationship("User", back_populates="uploaded_resumes")

    def __repr__(self):
        return f"<UploadedResume uuid={self.uuid} filename={self.original_filename} status={self.import_status}>"
