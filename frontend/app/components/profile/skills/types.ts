// filepath: frontend/app/components/profile/skills/types.ts
import type { Skill as BaseSkill } from '@/types/profile'

export type Skill = BaseSkill

export interface SkillFormData {
  category: string
  name: string
  proficiency: string
}

// Grouped skills for better display
export interface SkillGroup {
  category: string
  skills: Skill[]
  count: number
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
  { value: 'Beginner', label: 'Beginner', description: 'Basic understanding' },
  { value: 'Intermediate', label: 'Intermediate', description: 'Some experience' },
  { value: 'Advanced', label: 'Advanced', description: 'Extensive experience' },
  { value: 'Expert', label: 'Expert', description: 'Deep expertise' }
] as const
