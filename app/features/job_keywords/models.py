from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

from shared.models.base import Base

class JobKeyword(Base):
    __tablename__ = 'job_keywords'
    
    id = Column(Integer, primary_key=True)
    job_description_id = Column(Integer, ForeignKey('job_descriptions.id'))
    keyword = Column(String)
    
    job_description = relationship("JobDescription", back_populates="job_keywords")