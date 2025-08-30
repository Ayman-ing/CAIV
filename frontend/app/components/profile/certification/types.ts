// filepath: frontend/app/components/profile/certification/types.ts
// Certification TypeScript interfaces matching backend Certificate model

export interface Certificate {
  id?: number
  profileId?: number
  name: string
  issuer: string
  issueDate: string // ISO date string
  expirationDate?: string // ISO date string, nullable for non-expiring certs
  credentialId?: string
  credentialUrl?: string
  createdAt?: string
  updatedAt?: string
}

export interface CertificationFormData {
  name: string
  issuer: string
  issueDate: string
  expirationDate: string
  credentialId: string
  credentialUrl: string
  neverExpires: boolean
}

export interface CertificationValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface CertificationState {
  items: Certificate[]
  isLoading: boolean
  isSaving: boolean
  error: string | null
}

// For display and status tracking
export interface CertificationDisplay extends Certificate {
  displayIssueDate: string
  displayExpirationDate?: string
  isExpired: boolean
  isExpiringSoon: boolean // Within 30 days
  daysUntilExpiration?: number
  hasCredentialUrl: boolean
  status: 'active' | 'expired' | 'expiring-soon'
}

// Common certification providers
export const CERTIFICATION_PROVIDERS = [
  'AWS',
  'Microsoft',
  'Google Cloud',
  'Cisco',
  'CompTIA',
  'PMI',
  'Salesforce',
  'Oracle',
  'IBM',
  'Red Hat',
  'VMware',
  'Other'
] as const

// Certification categories
export const CERTIFICATION_CATEGORIES = [
  'Cloud Computing',
  'Cybersecurity',
  'Data & Analytics',
  'Project Management',
  'Software Development',
  'Networking',
  'IT Infrastructure',
  'DevOps',
  'AI/Machine Learning',
  'Other'
] as const
