// filepath: frontend/app/components/profile/custom/types.ts
import type { CustomSection as BaseCustomSection } from '@/types/profile'

export type CustomSection = BaseCustomSection

export interface CustomSectionFormData {
  title: string
  content: string
}

export interface CustomSectionDisplay extends CustomSection {
  // Add any display-specific properties here
}
