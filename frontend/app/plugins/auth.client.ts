// Auth plugin - Initialize auth state on app start
export default defineNuxtPlugin(async () => {
  const { authService } = await import('~/services/authService')
  const { useUserStore } = await import('~/stores/userStore')
  const store = useUserStore()
  
  
  // Load user preferences
  store.updatePreferences(store.preferences.value)
  
  // Check if user is authenticated (token exists and is valid)
  await authService.checkAuthStatus()
  
  // Fetch user profiles upon hard refresh if auth succeeded
  if (store.isAuthenticated.value) {
    const { profileService } = await import('~/services/profileService')
    try {
      await profileService.fetchUserProfiles()
    } catch (e) {
      console.error("Failed to fetch initial profile", e)
    }
  }
})
