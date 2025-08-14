// Authentication composable using Composition API

import type { User, AuthState, LoginRequest, RegisterRequest, ChangePasswordRequest, ApiError } from '~/types/auth'
import { authApi } from '~/api/auth'

// Global authentication state
const authState = reactive<AuthState>({
  user: null,
  isAuthenticated: false,
  isLoading: false,
})

// Track initialization state
const isInitialized = ref(false)

// Token management
const getStoredToken = (): string | null => {
  if (process.client) {
    return localStorage.getItem('access_token')
  }
  return null
}

const setStoredToken = (token: string): void => {
  if (process.client) {
    localStorage.setItem('access_token', token)
  }
}

const removeStoredToken = (): void => {
  if (process.client) {
    localStorage.removeItem('access_token')
  }
}

// Authentication actions
const login = async (credentials: LoginRequest): Promise<void> => {
  authState.isLoading = true
  try {
    const response = await authApi.login(credentials)
    
    // Store the JWT token
    setStoredToken(response.access_token)
    
    // Set user data
    authState.user = response.user
    authState.isAuthenticated = true
    
    // Navigate to dashboard
    await navigateTo('/dashboard')
  } catch (error) {
    authState.isAuthenticated = false
    authState.user = null
    throw error as ApiError
  } finally {
    authState.isLoading = false
  }
}

const register = async (userData: RegisterRequest): Promise<void> => {
  authState.isLoading = true
  try {
    const response = await authApi.register(userData)
    
    // Store the JWT token
    setStoredToken(response.access_token)
    
    // Set user data
    authState.user = response.user
    authState.isAuthenticated = true
    
    // Navigate to dashboard
    await navigateTo('/dashboard')
  } catch (error) {
    authState.isAuthenticated = false
    authState.user = null
    throw error as ApiError
  } finally {
    authState.isLoading = false
  }
}

const logout = async (): Promise<void> => {
  authState.isLoading = true
  try {
    await authApi.logout()
  } catch (error) {
    console.error('Logout error:', error)
  } finally {
    // Clear state and token regardless of API call success
    removeStoredToken()
    authState.user = null
    authState.isAuthenticated = false
    authState.isLoading = false
    
    // Navigate to home
    await navigateTo('/')
  }
}

const changePassword = async (passwordData: ChangePasswordRequest): Promise<void> => {
  authState.isLoading = true
  try {
    await authApi.changePassword(passwordData)
  } catch (error) {
    throw error as ApiError
  } finally {
    authState.isLoading = false
  }
}

const updateProfile = async (userData: Partial<User>): Promise<void> => {
  authState.isLoading = true
  try {
    const updatedUser = await authApi.updateProfile(userData)
    authState.user = updatedUser
  } catch (error) {
    throw error as ApiError
  } finally {
    authState.isLoading = false
  }
}

const getCurrentUser = async (): Promise<void> => {
  authState.isLoading = true
  try {
    const user = await authApi.getCurrentUser()
    authState.user = user
    authState.isAuthenticated = true
  } catch (error) {
    // If user fetch fails, user is not authenticated
    authState.user = null
    authState.isAuthenticated = false
  } finally {
    authState.isLoading = false
  }
}

const checkAuth = async (): Promise<void> => {
  // This will be called on app initialization to check if user is authenticated
  // Check if we have a stored token
  const token = getStoredToken()
  
  if (!token) {
    // No token, user is not authenticated
    authState.user = null
    authState.isAuthenticated = false
    isInitialized.value = true
    return
  }
  
  try {
    await getCurrentUser()
  } catch (error) {
    // Token is invalid, clear it
    removeStoredToken()
    authState.user = null
    authState.isAuthenticated = false
  } finally {
    // Mark as initialized
    isInitialized.value = true
  }
}

const deleteAccount = async (): Promise<void> => {
  authState.isLoading = true
  try {
    const token = getStoredToken()
    
    // Call delete user endpoint
    await $fetch(`/api/v1/me`, {
      method: 'DELETE',
      headers: token ? { 'Authorization': `Bearer ${token}` } : {},
      baseURL: useRuntimeConfig().public.apiBase
    })
    
    // Clear state and token and redirect
    removeStoredToken()
    authState.user = null
    authState.isAuthenticated = false
    await navigateTo('/')
  } catch (error) {
    throw error as ApiError
  } finally {
    authState.isLoading = false
  }
}

// Computed getters
const isAuthenticated = computed(() => authState.isAuthenticated)
const user = computed(() => authState.user)
const isLoading = computed(() => authState.isLoading)
const isAdmin = computed(() => authState.user?.role === 'admin')
const userName = computed(() => {
  if (!authState.user) return ''
  return `${authState.user.first_name} ${authState.user.last_name}`
})

// Helper function to wait for auth initialization
const waitForInitialization = async (): Promise<void> => {
  return new Promise((resolve) => {
    if (isInitialized.value) {
      resolve()
      return
    }
    
    const unwatch = watch(isInitialized, (newValue) => {
      if (newValue) {
        unwatch()
        resolve()
      }
    })
  })
}

// Main composable function
export const useAuth = () => {
  return {
    // State
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    isLoading: readonly(isLoading),
    isAdmin: readonly(isAdmin),
    userName: readonly(userName),
    isInitialized: readonly(isInitialized),
    
    // Actions
    login,
    register,
    logout,
    changePassword,
    updateProfile,
    getCurrentUser,
    checkAuth,
    deleteAccount,
    waitForInitialization,
  }
}

// For backward compatibility (temporary)
export const useAuthStore = useAuth
