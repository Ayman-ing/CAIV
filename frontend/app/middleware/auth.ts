import { useUserStore } from "~/stores/userStore"

// Authentication middleware - protects routes that require authentication
export default defineNuxtRouteMiddleware((to) => {
  const userStore = useUserStore()

  if (!userStore.isAuthenticated.value) {
    return navigateTo('/login')
  }
})
