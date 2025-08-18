// Guest middleware - redirects authenticated users away from login/register pages
import { useUserStore } from "~/stores/userStore"
export default defineNuxtRouteMiddleware((to) => {
  const { isAuthenticated } = useUserStore()
  
  if (isAuthenticated.value) {
    return navigateTo('/dashboard')
  }
})
