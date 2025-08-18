<script setup lang="ts">
import { useUserStore } from '~/stores/userStore'
import { authService } from '~/services/authService'

const userStore = useUserStore()
const { logout } = authService

// Use existing dark mode composable
const { isDark, toggle: toggleDarkMode } = useDarkMode()

// State for mobile menu and user dropdown
const mobileMenuOpen = ref(false)
const userMenuOpen = ref(false)

// Toggle mobile menu
const toggleMobileMenu = () => {
  mobileMenuOpen.value = !mobileMenuOpen.value
}

// Toggle user menu
const toggleUserMenu = () => {
  userMenuOpen.value = !userMenuOpen.value
}

// Handle logout
const handleLogout = async () => {
  try {
    await logout()
  } catch (error) {
    console.error('Logout error:', error)
  }
}

// User display helpers
const userInitials = computed(() => userStore.userInitials || 'U')
const userName = computed(() => userStore.userName || 'User')
const userEmail = computed(() => {
  const user = userStore.user
  return user?.value?.email || 'user@example.com'
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Simple Top Bar -->
    <div class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between items-center h-16">
          <!-- Logo -->
          <div class="flex items-center space-x-3">
            <div class="w-10 h-10 bg-gradient-to-br from-blue-600 to-blue-500 rounded-xl flex items-center justify-center">
                <img src="../../public/logo.png"  class="w-8 h-8" />
                </div>
            <div>
              <h1 class="text-lg font-bold text-gray-900 dark:text-white">
                CAIV
              </h1>
            </div>
          </div>

          <!-- Top Corner Controls -->
          <div class="flex items-center space-x-3">
            <!-- Dark Mode Toggle -->
            <button
              @click="toggleDarkMode"
              class="p-2 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="Toggle dark mode"
            >
              <Icon 
                :name="isDark ? 'mdi:weather-sunny' : 'mdi:weather-night'" 
                class="text-lg" 
              />
            </button>

            <!-- Logout Button -->
            <button
              @click="handleLogout"
              class="flex items-center space-x-2 px-3 py-2 text-gray-600 hover:text-red-600 dark:text-gray-400 dark:hover:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/30 rounded-lg transition-colors"
              title="Sign out"
            >
              <Icon name="mdi:logout" class="text-lg" />
              <span class="hidden sm:block font-medium">Sign Out</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Main Content -->
    <main class="flex-1">
      <slot />
    </main>
  </div>
</template>
