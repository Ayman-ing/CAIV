// filepath: frontend/app/components/profile/project/types.ts
// Projects TypeScript interfaces matching backend Project model

export interface Project {
  id?: number
  profileId?: number
  title: string
  description?: string
  startDate: string // ISO date string
  endDate?: string // ISO date string, nullable for ongoing projects
  projectUrl?: string
  createdAt?: string
  updatedAt?: string
}

export interface ProjectFormData {
  title: string
  description: string
  startDate: string
  endDate: string
  projectUrl: string
  isOngoing: boolean
}

// For project technologies and features
export interface ProjectTechnology {
  id: string
  name: string
  category: 'frontend' | 'backend' | 'database' | 'tool' | 'other'
}

export interface ProjectFeature {
  id: string
  description: string
  isHighlight: boolean
}

export interface ProjectValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface ProjectState {
  items: Project[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and enhanced project information
export interface ProjectDisplay extends Project {
  displayDateRange: string
  durationMonths: number
  durationText: string
  isOngoing: boolean
  technologies: ProjectTechnology[]
  features: ProjectFeature[]
  hasValidUrl: boolean
}

// Project categories for filtering/grouping
export const PROJECT_CATEGORIES = [
  'Web Development',
  'Mobile Development',
  'Data Science',
  'Machine Learning',
  'DevOps',
  'Desktop Application',
  'API Development',
  'Open Source',
  'Research',
  'Other'
] as const

// Project status options
export const PROJECT_STATUS = [
  { value: 'completed', label: 'Completed' },
  { value: 'ongoing', label: 'In Progress' },
  { value: 'paused', label: 'On Hold' },
  { value: 'archived', label: 'Archived' }
] as const
