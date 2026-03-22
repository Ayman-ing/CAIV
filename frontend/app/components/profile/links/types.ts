// filepath: frontend/app/components/profile/links/types.ts
import type { ProfileLink as BaseProfileLink } from '@/types/profile'

export type ProfileLink = BaseProfileLink

export interface LinkFormData {
  label: string
  url: string
  platform: string
  is_visible: boolean
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
    isProfessional: true
  },
  {
    value: 'github',
    label: 'GitHub',
    icon: 'mdi:github',
    placeholder: 'https://github.com/your-username',
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
    value: 'twitter',
    label: 'Twitter/X',
    icon: 'mdi:twitter',
    placeholder: 'https://twitter.com/your-handle',
    isProfessional: false
  },
  {
    value: 'other',
    label: 'Other',
    icon: 'mdi:link',
    placeholder: 'https://your-website.com',
    isProfessional: false
  }
] as const
