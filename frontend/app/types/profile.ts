// filepath: frontend/app/types/profile.ts
// TypeScript interfaces matching the backend SQLAlchemy models

export interface ProfileBasicInfo {
  id?: number
  name: string
  email: string
  phoneNumber: string
  location: string
  createdAt?: string
  updatedAt?: string
}

export interface Education {
  id?: number
  profileId?: number
  institution: string
  degree: string
  fieldOfStudy: string
  honors?: string
  gpa?: number
  startDate: string // ISO date string
  endDate?: string // ISO date string, nullable for ongoing
  description?: string
  createdAt?: string
  updatedAt?: string
}

export interface WorkExperience {
  id?: number
  profileId?: number
  jobTitle: string
  company: string
  startDate: string // ISO date string
  endDate?: string // ISO date string, nullable for current position
  description: string
  createdAt?: string
  updatedAt?: string
}

export interface Skill {
  id?: number
  profileId?: number
  category: string
  name: string
  proficiency: string // e.g., "Beginner", "Intermediate", "Advanced", "Expert"
  createdAt?: string
  updatedAt?: string
}

export interface Project {
  id?: number
  profileId?: number
  title: string
  description: string
  startDate: string // ISO date string
  endDate?: string // ISO date string, nullable for ongoing
  projectUrl?: string
  createdAt?: string
  updatedAt?: string
}

export interface Certificate {
  id?: number
  profileId?: number
  name: string
  issuer: string
  issueDate: string // ISO date string
  expirationDate?: string // ISO date string, nullable for non-expiring
  credentialId?: string
  credentialUrl?: string
  createdAt?: string
  updatedAt?: string
}

export interface Language {
  id?: number
  profileId?: number
  language: string
  proficiency: string // e.g., "Native", "Fluent", "Conversational", "Basic"
  createdAt?: string
  updatedAt?: string
}

export interface ProfessionalSummary {
  id?: number
  profileId?: number
  title: string
  summary: string
  isDefault?: boolean
  createdAt?: string
  updatedAt?: string
}

export interface ProfileLink {
  id?: number
  profileId?: number
  platform: string // e.g., "LinkedIn", "GitHub", "Portfolio", "Website"
  url: string
  displayName?: string
  isPublic?: boolean
  createdAt?: string
  updatedAt?: string
}

// Utility types for forms
export interface EducationFormData extends Omit<Education, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface WorkExperienceFormData extends Omit<WorkExperience, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface SkillFormData extends Omit<Skill, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface ProjectFormData extends Omit<Project, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface CertificateFormData extends Omit<Certificate, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface LanguageFormData extends Omit<Language, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}
export interface ProfileLinkFormData extends Omit<ProfileLink, 'id' | 'profileId' | 'createdAt' | 'updatedAt'> {}

// Constants for dropdowns and validation
export const PROFICIENCY_LEVELS = {
  SKILL: ['Beginner', 'Intermediate', 'Advanced', 'Expert'],
  LANGUAGE: ['Basic', 'Conversational', 'Fluent', 'Native']
} as const

export const SKILL_CATEGORIES = [
  'Programming Languages',
  'Frameworks & Libraries',
  'Databases',
  'Cloud & DevOps',
  'Design & UI/UX',
  'Project Management',
  'Soft Skills',
  'Other'
] as const

export const LINK_PLATFORMS = [
  'LinkedIn',
  'GitHub',
  'Portfolio',
  'Website',
  'Twitter',
  'Behance',
  'Dribbble',
  'Medium',
  'YouTube',
  'Other'
] as const

export const DEGREE_TYPES = [
  'High School Diploma',
  'Associate Degree',
  'Bachelor\'s Degree',
  'Master\'s Degree',
  'Doctoral Degree',
  'Certificate',
  'Diploma',
  'Other'
] as const
