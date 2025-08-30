// filepath: frontend/app/components/profile/language/types.ts
// Languages TypeScript interfaces matching backend Language model

export interface Language {
  id?: number
  profileId?: number
  language: string
  proficiency: string
  createdAt?: string
  updatedAt?: string
}

export interface LanguageFormData {
  language: string
  proficiency: string
}

export interface LanguageValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface LanguageState {
  items: Language[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and enhanced language information
export interface LanguageDisplay extends Language {
  nativeName?: string
  flag?: string
  proficiencyLevel: number // 1-5 scale
  canWorkIn: boolean // Professional level or above
}

// Proficiency levels following CEFR standards
export const PROFICIENCY_LEVELS = [
  { value: 'native', label: 'Native', level: 5, description: 'Native or bilingual proficiency' },
  { value: 'fluent', label: 'Fluent', level: 4, description: 'Full professional proficiency' },
  { value: 'professional', label: 'Professional', level: 3, description: 'Professional working proficiency' },
  { value: 'conversational', label: 'Conversational', level: 2, description: 'Limited working proficiency' },
  { value: 'basic', label: 'Basic', level: 1, description: 'Elementary proficiency' }
] as const

// Common languages with their native names and codes
export const COMMON_LANGUAGES = [
  { code: 'en', name: 'English', nativeName: 'English' },
  { code: 'es', name: 'Spanish', nativeName: 'Español' },
  { code: 'fr', name: 'French', nativeName: 'Français' },
  { code: 'de', name: 'German', nativeName: 'Deutsch' },
  { code: 'it', name: 'Italian', nativeName: 'Italiano' },
  { code: 'pt', name: 'Portuguese', nativeName: 'Português' },
  { code: 'ru', name: 'Russian', nativeName: 'Русский' },
  { code: 'zh', name: 'Chinese', nativeName: '中文' },
  { code: 'ja', name: 'Japanese', nativeName: '日本語' },
  { code: 'ko', name: 'Korean', nativeName: '한국어' },
  { code: 'ar', name: 'Arabic', nativeName: 'العربية' },
  { code: 'hi', name: 'Hindi', nativeName: 'हिन्दी' },
  { code: 'nl', name: 'Dutch', nativeName: 'Nederlands' },
  { code: 'sv', name: 'Swedish', nativeName: 'Svenska' },
  { code: 'no', name: 'Norwegian', nativeName: 'Norsk' },
  { code: 'da', name: 'Danish', nativeName: 'Dansk' },
  { code: 'fi', name: 'Finnish', nativeName: 'Suomi' }
] as const
