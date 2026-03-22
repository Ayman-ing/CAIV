// filepath: frontend/app/components/profile/certification/types.ts
import type { Certificate as BaseCertificate } from '@/types/profile'

export type Certificate = BaseCertificate

export interface CertificationFormData {
  name: string
  issuing_organization: string
  issue_date: string
  expiration_date: string
  credential_id: string
  neverExpires: boolean
}

// For display and status tracking
export interface CertificationDisplay extends Certificate {
  displayIssueDate: string
  displayExpirationDate?: string
  isExpired: boolean
  isExpiringSoon: boolean // Within 30 days
  daysUntilExpiration?: number
  status: 'active' | 'expired' | 'expiring-soon'
}

// Common certification providers
export const CERTIFICATION_PROVIDERS = [
  'AWS', 'Microsoft', 'Google Cloud', 'Cisco', 'CompTIA', 'PMI',
  'Salesforce', 'Oracle', 'IBM', 'Red Hat', 'VMware', 'Other'
] as const
