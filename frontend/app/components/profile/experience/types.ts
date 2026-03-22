// filepath: frontend/app/components/profile/experience/types.ts
import type { WorkExperience as BaseWorkExperience } from '@/types/profile'

export type WorkExperience = BaseWorkExperience

export interface ExperienceFormData {
  job_title: string
  company: string
  start_date: string
  end_date: string
  description: string
  isCurrentJob: boolean
}

// For achievements and responsibilities parsing
export interface ExperienceAchievement {
  id: string
  text: string
  isHighlight: boolean
}

export interface ExperienceValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface ExperienceState {
  items: WorkExperience[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and calculations
export interface ExperienceDisplay extends WorkExperience {
  displayDateRange: string
  durationText: string
  isCurrentPosition: boolean
}
