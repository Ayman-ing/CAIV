// filepath: frontend/app/components/profile/project/types.ts
import type { Project as BaseProject } from '@/types/profile'

export type Project = BaseProject

export interface ProjectFormData {
  name: string
  description: string
  technologies: string
  start_date: string
  end_date: string
  url: string
  isOngoing: boolean
}

// For display and enhanced project information
export interface ProjectDisplay extends Project {
  displayDateRange: string
  durationText: string
  isOngoing: boolean
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
