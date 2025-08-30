// Authentication API calls using Nuxt's $fetch

import type { 
  LoginRequest, 
  RegisterRequest, 
  ChangePasswordRequest,
  AuthResponse,
  User 
} from '~/components/auth/types'

// Helper function to get full API URL
const getApiUrl = (endpoint: string) => {
  const config = useRuntimeConfig()
  return `${config.public.apiBase}${endpoint}`
}

// Helper function to get authorization headers
const getAuthHeaders = (): Record<string, string> => {
  if (process.client) {
    const token = localStorage.getItem('access_token')
    if (token) {
      return {
        'Authorization': `Bearer ${token}`
      }
    }
  }
  return {}
}

export const authApi = {
  // Register new user
  async register(data: RegisterRequest): Promise<AuthResponse> {
    try {
      return await $fetch<AuthResponse>(getApiUrl('/api/v1/auth/register'), {
        method: 'POST',
        body: data,
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Registration failed'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Login user
  async login(loginData: LoginRequest): Promise<AuthResponse> {
    try {
      // Convert to form data for OAuth2PasswordRequestForm
      const formData = new FormData()
      formData.append('username', loginData.email) // FastAPI OAuth2 expects 'username'
      formData.append('password', loginData.password)

      return await $fetch<AuthResponse>(getApiUrl('/api/v1/auth/login'), {
        method: 'POST',
        body: formData,
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Login failed'
      throw createError({
        statusCode: error.statusCode || 401,
        statusMessage: errorMessage
      })
    }
  },

  // Logout user
  async logout(): Promise<void> {
    try {
      await $fetch<void>(getApiUrl('/api/v1/auth/logout'), {
        method: 'POST',
        headers: getAuthHeaders(),
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Logout failed'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Get current user profile
  async getCurrentUser(): Promise<User> {
    try {
      return await $fetch<User>(getApiUrl('/api/v1/me'), {
        method: 'GET',
        headers: getAuthHeaders(),
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Failed to fetch user data'
      throw createError({
        statusCode: error.statusCode || 401,
        statusMessage: errorMessage
      })
    }
  },

  // Update current user profile
  async updateProfile(userData: Partial<User>): Promise<User> {
    try {
      return await $fetch<User>(getApiUrl('/api/v1/me'), {
        method: 'PUT',
        body: userData,
        headers: getAuthHeaders(),
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Failed to update profile'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Change password
  async changePassword(data: ChangePasswordRequest): Promise<{ message: string }> {
    try {
      return await $fetch<{ message: string }>(getApiUrl('/api/v1/auth/change-password'), {
        method: 'POST',
        body: data,
        headers: getAuthHeaders(),
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Failed to change password'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Request password reset
  async requestPasswordReset(email: string): Promise<{ message: string }> {
    try {
      return await $fetch<{ message: string }>(getApiUrl('/api/v1/auth/request-password-reset'), {
        method: 'POST',
        body: { email },
        credentials: 'include',
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Failed to send reset email'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Reset password with token
  async resetPassword(token: string, newPassword: string, confirmPassword: string): Promise<{ message: string }> {
    try {
      return await $fetch<{ message: string }>(getApiUrl('/api/v1/auth/reset-password'), {
        method: 'POST',
        body: {
          token,
          new_password: newPassword,
          confirm_new_password: confirmPassword,
        },
        credentials: 'include',
      })
    } catch (error: any) {
      // Handle the new error format from backend
      const errorMessage = error.data?.error?.message || error.data?.message || error.message || 'Failed to reset password'
      throw createError({
        statusCode: error.statusCode || 400,
        statusMessage: errorMessage
      })
    }
  },

  // Check authentication status
  async checkAuth(): Promise<User | null> {
    try {
      return await $fetch<User>(getApiUrl('/api/v1/me'), {
        method: 'GET',
        credentials: 'include',
      })
    } catch (error) {
      // User is not authenticated
      return null
    }
  }
}
