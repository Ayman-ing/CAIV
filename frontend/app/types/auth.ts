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
}

export interface ApiError {
  error: {
    code : string,
    message : string
    details : { [key: string]: any }
  }
  path : string 
  method : string
}

// Password validation result
export interface PasswordValidation {
  isValid: boolean
  errors: string[]
  strength: 'weak' | 'medium' | 'strong'
}
