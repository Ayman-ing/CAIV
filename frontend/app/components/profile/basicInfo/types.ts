// filepath: frontend/app/components/profile/basicInfo/types.ts
// Basic Information TypeScript interfaces matching backend Profile model

export interface BasicInfo {
  id?: number
  name: string
  email: string
  phoneNumber: string
  location: string
  createdAt?: string
  updatedAt?: string
}

export interface BasicInfoFormData {
  fullName: string
  email: string
  phoneNumber: string
  location: string
}

// Form field configuration for completion tracking
export interface BasicInfoField {
  key: keyof BasicInfoFormData
  label: string
  value: string
  required: boolean
}

// Validation interfaces
export interface BasicInfoValidation {
  isValid: boolean
  errors: Record<string, string>
}

export interface BasicInfoState {
  data: BasicInfo | null
  isLoading: boolean
  isSaving: boolean
  error: string | null
}
