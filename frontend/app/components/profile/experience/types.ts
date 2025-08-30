// filepath: frontend/app/components/profile/experience/types.ts
// Work Experience TypeScript interfaces matching backend WorkExperience model

export interface WorkExperience {
  id?: number
  profileId?: number
  jobTitle: string
  company: string
  startDate: string // ISO date string
  endDate?: string // ISO date string, nullable for current job
  description?: string
  createdAt?: string
  updatedAt?: string
}

export interface ExperienceFormData {
  jobTitle: string
  company: string
  startDate: string
  endDate: string
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
  durationMonths: number
  durationText: string
  isCurrentPosition: boolean
  achievements: ExperienceAchievement[]
}

// For experience summary calculations
export interface ExperienceSummary {
  totalPositions: number
  totalYearsExperience: number
  currentPosition?: WorkExperience
  industries: string[]
}
