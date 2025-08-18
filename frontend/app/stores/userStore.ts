// User Store - Simple state management
import type { User } from '~/types/auth'

// Simple reactive state
const state = reactive({
  user: null as User | null,
  isLoading: false
})

// Token utilities
const getToken = (): string | null => {
  if (process.client) {
    return localStorage.getItem('access_token')
  }
  return null
}

const setToken = (token: string): void => {
  if (process.client) {
    localStorage.setItem('access_token', token)
  }
}

const removeToken = (): void => {
  if (process.client) {
    localStorage.removeItem('access_token')
  }
}

// User preferences (simple localStorage)
const loadPreferences = () => {
  if (process.client) {
    const stored = localStorage.getItem('user_preferences')
    try {
      return stored ? JSON.parse(stored) : { theme: 'system' }
    } catch {
      return { theme: 'system' }
    }
  }
  return { theme: 'system' }
}

const savePreferences = (prefs: any) => {
  if (process.client) {
    localStorage.setItem('user_preferences', JSON.stringify(prefs))
  }
}

export const useUserStore = () => {
  const preferences = ref(loadPreferences())

  return {
    // State
    user: computed(() => state.user),
    isLoading: computed(() => state.isLoading),
    preferences: readonly(preferences),
    
    // Computed
    isAuthenticated: computed(() => !!state.user),
    isAdmin: computed(() => state.user?.role === 'admin'),
    userName: computed(() => {
      if (!state.user) return ''
      return `${state.user.first_name} ${state.user.last_name}`
    }),
    userInitials: computed(() => {
      if (!state.user) return ''
      return `${state.user.first_name[0]}${state.user.last_name[0]}`.toUpperCase()
    }),
    
    // Actions
    login(user: User, token: string) {
      state.user = user
      setToken(token)
    },
    
    logout() {
      state.user = null
      removeToken()
    },
    
    setUser(user: User | null) {
      state.user = user
    },
    
    setLoading(loading: boolean) {
      state.isLoading = loading
    },
    
    updatePreferences(newPrefs: Partial<typeof preferences.value>) {
      preferences.value = { ...preferences.value, ...newPrefs }
      savePreferences(preferences.value)
    },
    
    // Token utilities
    getToken,
    hasToken: () => !!getToken()
  }
}
