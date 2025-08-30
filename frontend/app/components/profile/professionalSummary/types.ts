// filepath: frontend/app/components/profile/professionalSummary/types.ts
// Professional Summary TypeScript interfaces matching backend ProfessionalSummary model

export interface ProfessionalSummary {
  id?: number
  profileId?: number
  title: string
  content: string
  isDefault: boolean
  createdAt?: string
  updatedAt?: string
}

export interface ProfessionalSummaryFormData {
  title: string
  content: string
}

export interface SummaryValidation {
  isValid: boolean
  errors: Record<string, string>
  wordCount: number
  isOptimalLength: boolean
}

export interface SummaryState {
  items: ProfessionalSummary[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and analysis
export interface SummaryDisplay extends ProfessionalSummary {
  wordCount: number
  readingTime: number // in seconds
  isOptimalLength: boolean
  keywordsCount: number
  preview: string // First 100 characters
}

// Summary templates and suggestions
export interface SummaryTemplate {
  id: string
  title: string
  description: string
  template: string
  category: 'general' | 'technical' | 'creative' | 'management' | 'sales'
  targetRoles: string[]
}

// Common summary templates
export const SUMMARY_TEMPLATES: SummaryTemplate[] = [
  {
    id: 'software-engineer',
    title: 'Software Engineer',
    description: 'For software development roles',
    template: 'Experienced software engineer with [X] years of expertise in [technologies]. Proven track record of developing scalable applications and leading technical projects.',
    category: 'technical',
    targetRoles: ['Software Engineer', 'Developer', 'Backend Engineer', 'Full Stack Engineer']
  },
  {
    id: 'data-scientist',
    title: 'Data Scientist',
    description: 'For data science and analytics roles',
    template: 'Data scientist with expertise in machine learning and statistical analysis. Skilled in [tools/languages] with experience in extracting actionable insights from complex datasets.',
    category: 'technical',
    targetRoles: ['Data Scientist', 'Data Analyst', 'ML Engineer']
  },
  {
    id: 'project-manager',
    title: 'Project Manager',
    description: 'For project management roles',
    template: 'Results-driven project manager with [X] years of experience leading cross-functional teams. Proven ability to deliver projects on time and within budget.',
    category: 'management',
    targetRoles: ['Project Manager', 'Program Manager', 'Scrum Master']
  },
  {
    id: 'generic',
    title: 'General Professional',
    description: 'Adaptable for various roles',
    template: 'Dedicated professional with [X] years of experience in [industry/field]. Strong background in [key skills] with a proven track record of achieving results.',
    category: 'general',
    targetRoles: []
  }
] as const

// Writing guidelines
export const SUMMARY_GUIDELINES = {
  minWords: 50,
  maxWords: 150,
  optimalWords: { min: 80, max: 120 },
  maxCharacters: 600
} as const
