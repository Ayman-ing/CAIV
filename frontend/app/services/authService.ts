// Authentication Service - Simple functions approach
import type { User, LoginRequest, RegisterRequest, ChangePasswordRequest, AuthError as ApiError } from '~/components/auth/types'
import { authApi } from '~/api/auth'
import { useUserStore } from '~/stores/userStore'

export const authService = {
  async login(credentials: LoginRequest): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      const response = await authApi.login(credentials)
      
      // Store token temporarily
      if (process.client) {
        localStorage.setItem('access_token', response.access_token)
      }
      
      // Fetch user data using the token
      const userData = await authApi.getCurrentUser()
      
      // Now set the complete user state
      userStore.login(userData, response.access_token)
            await navigateTo('/dashboard')
    } catch (error) {
      userStore.logout()
      throw error as ApiError
    } finally {
      userStore.setLoading(false)
    }
  },

  async register(userData: RegisterRequest): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      const response = await authApi.register(userData)
      
      // Store token temporarily
      if (process.client) {
        localStorage.setItem('access_token', response.access_token)
      }
      
      // Fetch user data using the token
      const userDataResponse = await authApi.getCurrentUser()
      
      userStore.login(userDataResponse, response.access_token)
      await navigateTo('/dashboard')
    } catch (error) {
      userStore.logout()
      throw error as ApiError
    } finally {
      userStore.setLoading(false)
    }
  },

  async logout(): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      await authApi.logout()
    } catch (error) {
      console.error('Logout error:', error)
    } finally {
      userStore.logout()
      userStore.setLoading(false)
      await navigateTo('/')
    }
  },

  async changePassword(passwordData: ChangePasswordRequest): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      await authApi.changePassword(passwordData)
    } catch (error) {
      throw error as ApiError
    } finally {
      userStore.setLoading(false)
    }
  },

  async updateProfile(userData: Partial<User>): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      const updatedUser = await authApi.updateProfile(userData)
      userStore.setUser(updatedUser)
    } catch (error) {
      throw error as ApiError
    } finally {
      userStore.setLoading(false)
    }
  },

  async getCurrentUser(): Promise<void> {
    const userStore = useUserStore()

    userStore.setLoading(true)
    
    try {
      const user = await authApi.getCurrentUser()
      userStore.setUser(user)
    } catch (error) {
      userStore.logout()
      throw error
    } finally {
      userStore.setLoading(false)
    }
  },

  async checkAuthStatus(): Promise<void> {    
    const userStore = useUserStore()

    // Check if we have a stored token
    if (!userStore.hasToken()) {
      userStore.logout()
      return
    }
    
    try {
      await this.getCurrentUser()
    } catch (error) {
      // Token is invalid, clear it
      userStore.logout()
    }
  },



}
