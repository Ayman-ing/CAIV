// filepath: frontend/app/components/profile/links/types.ts
// Profile Links TypeScript interfaces matching backend ProfileLink model

export interface ProfileLink {
  id?: number
  profileId?: number
  label: string
  url: string
  linkType: string
  isVisible: boolean
  displayOrder?: number
  createdAt?: string
  updatedAt?: string
}

export interface LinkFormData {
  label: string
  url: string
  linkType: string
  isVisible: boolean
}

export interface LinkValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface LinkState {
  items: ProfileLink[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and enhanced link information
export interface LinkDisplay extends ProfileLink {
  icon: string
  domain: string
  isValidUrl: boolean
  isProfessional: boolean
  displayUrl: string // Formatted for display
}

// Link types with their configurations
export interface LinkTypeConfig {
  value: string
  label: string
  icon: string
  placeholder: string
  validator?: RegExp
  isProfessional: boolean
}

// Predefined link types
export const LINK_TYPES: LinkTypeConfig[] = [
  {
    value: 'linkedin',
    label: 'LinkedIn',
    icon: 'mdi:linkedin',
    placeholder: 'https://linkedin.com/in/your-profile',
    validator: /^https?:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$/,
    isProfessional: true
  },
  {
    value: 'github',
    label: 'GitHub',
    icon: 'mdi:github',
    placeholder: 'https://github.com/your-username',
    validator: /^https?:\/\/(www\.)?github\.com\/[a-zA-Z0-9-]+\/?$/,
    isProfessional: true
  },
  {
    value: 'portfolio',
    label: 'Portfolio',
    icon: 'mdi:web',
    placeholder: 'https://your-portfolio.com',
    isProfessional: true
  },
  {
    value: 'behance',
    label: 'Behance',
    icon: 'mdi:behance',
    placeholder: 'https://behance.net/your-profile',
    validator: /^https?:\/\/(www\.)?behance\.net\/[a-zA-Z0-9-]+\/?$/,
    isProfessional: true
  },
  {
    value: 'dribbble',
    label: 'Dribbble',
    icon: 'mdi:dribbble',
    placeholder: 'https://dribbble.com/your-profile',
    validator: /^https?:\/\/(www\.)?dribbble\.com\/[a-zA-Z0-9-]+\/?$/,
    isProfessional: true
  },
  {
    value: 'twitter',
    label: 'Twitter/X',
    icon: 'mdi:twitter',
    placeholder: 'https://twitter.com/your-handle',
    validator: /^https?:\/\/(www\.)?(twitter|x)\.com\/[a-zA-Z0-9_]+\/?$/,
    isProfessional: false
  },
  {
    value: 'stackoverflow',
    label: 'Stack Overflow',
    icon: 'mdi:stack-overflow',
    placeholder: 'https://stackoverflow.com/users/your-id',
    isProfessional: true
  },
  {
    value: 'medium',
    label: 'Medium',
    icon: 'mdi:medium',
    placeholder: 'https://medium.com/@your-username',
    isProfessional: true
  },
  {
    value: 'other',
    label: 'Other',
    icon: 'mdi:link',
    placeholder: 'https://your-website.com',
    isProfessional: false
  }
] as const
