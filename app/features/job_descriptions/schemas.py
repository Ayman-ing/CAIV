"""
Job Description Schemas

Pydantic schemas for job description data validation.
"""

from pydantic import BaseModel, HttpUrl, Field, validator
from datetime import datetime
from typing import Optional, List
import uuid
import re


class JobDescriptionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255, description="Job title")
    company: str = Field(..., min_length=1, max_length=255, description="Company name")
    url: HttpUrl = Field(..., description="URL to the job posting")
    content: Optional[str] = Field(None, max_length=50000, description="Raw job description content")
    requirements: Optional[List[str]] = Field(default=[], description="Parsed job requirements")
    skills: Optional[List[str]] = Field(default=[], description="Extracted required skills")
    location: Optional[str] = Field(None, max_length=255, description="Job location")
    salary_range: Optional[str] = Field(None, max_length=100, description="Salary range if provided")
    employment_type: Optional[str] = Field(None, max_length=50, description="Employment type (full-time, part-time, etc.)")

    @validator('title')
    def validate_title(cls, v):
        if not v.strip():
            raise ValueError('Job title cannot be empty or whitespace only')
        return v.strip()

    @validator('company')
    def validate_company(cls, v):
        if not v.strip():
            raise ValueError('Company name cannot be empty or whitespace only')
        return v.strip()

    @validator('url')
    def validate_job_url(cls, v):
        url_str = str(v)
        # Basic validation for job posting URLs
        job_domains = [
            'linkedin.com', 'indeed.com', 'glassdoor.com', 'monster.com',
            'ziprecruiter.com', 'careerbuilder.com', 'simplyhired.com',
            'jobs.com', 'workday.com', 'greenhouse.io', 'lever.co',
            'careers.', 'jobs.'  # Common career page patterns
        ]
        
        # Allow any HTTPS URL but warn if it's not from known job sites
        if not any(domain in url_str.lower() for domain in job_domains):
            # Still valid, just not from a known job site
            pass
            
        return v

    @validator('requirements', 'skills', pre=True)
    def validate_lists(cls, v):
        if v is None:
            return []
        if isinstance(v, str):
            # Split by common delimiters if string provided
            return [item.strip() for item in re.split(r'[,;\n]', v) if item.strip()]
        return v


class JobDescriptionCreate(JobDescriptionBase):
    pass


class JobDescriptionUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    company: Optional[str] = Field(None, min_length=1, max_length=255)
    url: Optional[HttpUrl] = None
    content: Optional[str] = Field(None, max_length=50000)
    requirements: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    location: Optional[str] = Field(None, max_length=255)
    salary_range: Optional[str] = Field(None, max_length=100)
    employment_type: Optional[str] = Field(None, max_length=50)

    @validator('title')
    def validate_title(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Job title cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('company')
    def validate_company(cls, v):
        if v is not None and not v.strip():
            raise ValueError('Company name cannot be empty or whitespace only')
        return v.strip() if v else v

    @validator('requirements', 'skills', pre=True)
    def validate_lists(cls, v):
        if v is None:
            return v
        if isinstance(v, str):
            return [item.strip() for item in re.split(r'[,;\n]', v) if item.strip()]
        return v


class JobDescriptionResponse(JobDescriptionBase):
    uuid: uuid.UUID
    user_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
