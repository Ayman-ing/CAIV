// filepath: frontend/app/components/profile/skills/types.ts
// Skills TypeScript interfaces matching backend Skill model

export interface Skill {
  id?: number
  profileId?: number
  category: string
  name: string
  proficiency: string
  createdAt?: string
  updatedAt?: string
}

export interface SkillFormData {
  category: string
  name: string
  proficiency: string
}

// Predefined skill categories and proficiency levels
export interface SkillOptions {
  categories: string[]
  proficiencyLevels: { value: string; label: string; description?: string }[]
}

// Grouped skills for better display
export interface SkillGroup {
  category: string
  skills: Skill[]
  count: number
}

export interface SkillValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface SkillState {
  items: Skill[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For skill suggestions and auto-complete
export interface SkillSuggestion {
  name: string
  category: string
  popularity: number
  isRecommended: boolean
}

// Common skill categories
export const SKILL_CATEGORIES = [
  'Programming Languages',
  'Frameworks & Libraries',
  'Databases',
  'Cloud & DevOps',
  'Tools & Software',
  'Operating Systems',
  'Soft Skills',
  'Languages',
  'Other'
] as const

// Common proficiency levels
export const PROFICIENCY_LEVELS = [
  { value: 'beginner', label: 'Beginner', description: 'Basic understanding' },
  { value: 'intermediate', label: 'Intermediate', description: 'Some experience' },
  { value: 'advanced', label: 'Advanced', description: 'Extensive experience' },
  { value: 'expert', label: 'Expert', description: 'Deep expertise' }
] as const
