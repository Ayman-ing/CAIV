// Authentication middleware - protects routes that require authentication

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Import the composable within the middleware
  const { useAuth } = await import('~/composables/useAuth')
  const { isAuthenticated, waitForInitialization } = useAuth()
  
  // Wait for auth initialization to complete
  await waitForInitialization()
  
  // If not authenticated, redirect to login
  if (!isAuthenticated.value) {
    return navigateTo('/login')
  }
})
