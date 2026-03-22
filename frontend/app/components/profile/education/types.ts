// filepath: frontend/app/components/profile/education/types.ts
import type { Education as BaseEducation } from '@/types/profile'

export type Education = BaseEducation

export interface EducationFormData {
  institution: string
  degree: string
  degree_type: string
  field_of_study: string
  honors: string
  gpa: string // String for form handling
  start_date: string
  end_date: string
  description: string
  isOngoing: boolean
}

// Predefined options for dropdowns
export interface EducationOptions {
  degreeTypes: string[]
  gpaScales: { value: string; label: string }[]
}

export interface EducationDisplay extends Education {
  displayDateRange: string
  isCompleted: boolean
  completionYear?: number
}
