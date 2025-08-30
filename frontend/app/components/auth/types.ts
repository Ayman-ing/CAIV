// filepath: frontend/app/components/auth/types.ts
// Authentication related TypeScript interfaces

export interface User {
  uuid: string
  email: string
  first_name: string
  last_name: string
  role: 'user' | 'admin'
  is_active: boolean
  is_verified: boolean
  created_at: string
  updated_at: string
}

export interface LoginRequest {
  email: string
  password: string
}

export interface RegisterRequest {
  email: string
  password: string
  confirm_password: string
  first_name: string
  last_name: string
}

export interface ChangePasswordRequest {
  current_password: string
  new_password: string
  confirm_new_password: string
}

export interface AuthResponse {
  user: User
  access_token: string
  token_type: string
  expires_in: number
}

export interface TokenData {
  user_id: string
  role: string
  exp: number
  iat: number
}

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
  token: string | null
}

export interface AuthError {
  message: string
  field?: string
  code?: string
}

// Form validation interfaces
export interface LoginFormData {
  email: string
  password: string
}

export interface RegisterFormData {
  email: string
  password: string
  confirm_password: string
  first_name: string
  last_name: string
}

// Validation error interfaces
export interface ValidationError {
  field: string
  message: string
}

export interface FormErrors {
  [key: string]: string
}
