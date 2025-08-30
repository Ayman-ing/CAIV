// filepath: frontend/app/components/profile/education/types.ts
// Education TypeScript interfaces matching backend Education model

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

export interface EducationFormData {
  institution: string
  degree: string
  fieldOfStudy: string
  honors: string
  gpa: string // String for form handling, converted to number on save
  startDate: string
  endDate: string
  description: string
  isOngoing: boolean
}

// Predefined options for dropdowns
export interface EducationOptions {
  degreeTypes: string[]
  gpaScales: { value: string; label: string }[]
}

export interface EducationValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface EducationState {
  items: Education[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and sorting
export interface EducationDisplay extends Education {
  displayDateRange: string
  isCompleted: boolean
  completionYear?: number
}
