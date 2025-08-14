// Auth plugin to initialize authentication state

export default defineNuxtPlugin(async () => {
  // Import the composable within the plugin
  const { useAuth } = await import('~/composables/useAuth')
  const { checkAuth, isAuthenticated, user } = useAuth()
  
  console.log('Auth plugin - starting initialization')
  
  // Check authentication status on app initialization
  // This will verify if user has valid httpOnly session cookie
  await checkAuth()
  
  console.log('Auth plugin - initialization complete')
  console.log('Auth plugin - isAuthenticated:', isAuthenticated.value)
  console.log('Auth plugin - user:', user.value)
})
