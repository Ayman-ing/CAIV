// Guest middleware - redirects authenticated users away from login/register pages

export default defineNuxtRouteMiddleware(async (to, from) => {
  // Import the composable within the middleware
  const { useAuth } = await import('~/composables/useAuth')
  const { isAuthenticated, waitForInitialization, user } = useAuth()
  
  // Wait for auth initialization to complete
  await waitForInitialization()
  
  // Debug logging
  console.log('Guest middleware - isAuthenticated:', isAuthenticated.value)
  console.log('Guest middleware - user:', user.value)
  console.log('Guest middleware - target route:', to.path)
  
  // If user is already authenticated, redirect to dashboard
  if (isAuthenticated.value) {
    console.log('Guest middleware - redirecting to dashboard')
    return navigateTo('/dashboard')
  }
  
  console.log('Guest middleware - allowing access to', to.path)
})
