// filepath: frontend/app/types/profile.ts

export interface Profile {
  uuid: string
  user_id: number
  name: string | null
  email: string | null
  phone_number: string | null
  location: string | null
  created_at: string
  updated_at: string
}

// Profile Sections
export interface Education {
  uuid: string
  institution: string
  degree: string
  degree_type?: string
  field_of_study: string | null
  honors: string | null
  gpa: number | null
  start_date: string
  end_date: string | null
  description: string | null
  created_at?: string
  updated_at?: string
}

export interface WorkExperience {
  uuid: string
  job_title: string
  company: string
  description: string | null
  start_date: string
  end_date: string | null
  created_at?: string
  updated_at?: string
}

export interface Project {
  uuid: string
  name: string
  description: string | null
  technologies: string | null
  start_date: string
  end_date: string | null
  url: string | null
  created_at?: string
  updated_at?: string
}

export interface Skill {
  uuid: string
  name: string
  category: string | null
  proficiency: string | null
  years_experience?: number | null
  created_at?: string
  updated_at?: string
}

export interface Certificate {
  uuid: string
  name: string
  issuing_organization: string
  issue_date: string
  expiration_date: string | null
  credential_id: string | null
  created_at?: string
  updated_at?: string
}

export interface Language {
  uuid: string
  language: string
  proficiency: string
  can_read?: boolean
  can_write?: boolean
  can_speak?: boolean
  created_at?: string
  updated_at?: string
}

export interface ProfessionalSummary {
  uuid: string
  title: string
  content: string
  is_default: boolean
  created_at?: string
  updated_at?: string
}

export interface ProfileLink {
  uuid: string
  label: string
  url: string
  platform: string
  is_visible: boolean
  created_at?: string
  updated_at?: string
}

export interface CustomSection {
  uuid: string
  title: string
  content: string
  order_index?: number
  created_at?: string
  updated_at?: string
}

export type ProfileCreate = Omit<Profile, 'uuid' | 'user_id' | 'created_at' | 'updated_at'>
export type ProfileUpdate = Partial<ProfileCreate>
