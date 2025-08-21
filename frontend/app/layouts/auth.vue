<script setup lang="ts">
// filepath: frontend/app/layouts/auth.vue
import { useUserStore } from '~/stores/userStore'
import { useDarkMode } from '~/composables/useDarkMode'

const { user, userInitials, logout } = useUserStore()
const { toggle } = useDarkMode()

// Mobile menu state
const isMobileMenuOpen = ref(false)
// User dropdown state
const isUserDropdownOpen = ref(false)

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const toggleUserDropdown = () => {
  isUserDropdownOpen.value = !isUserDropdownOpen.value
}

const handleLogout = async () => {
  await logout()
  await navigateTo('/login')
}

const navigateToProfile = () => {
  isUserDropdownOpen.value = false
  navigateTo('/profile')
}

// Close dropdown when clicking outside
onMounted(() => {
  const closeDropdown = (event: MouseEvent) => {
    const dropdown = document.getElementById('user-dropdown')
    const button = document.getElementById('user-menu-button')
    
    if (dropdown && button && 
        !dropdown.contains(event.target as Node) && 
        !button.contains(event.target as Node)) {
      isUserDropdownOpen.value = false
    }
  }

  document.addEventListener('click', closeDropdown)
  
  onUnmounted(() => {
    document.removeEventListener('click', closeDropdown)
  })
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900">
    <!-- Navigation Header -->
    <nav class="bg-white dark:bg-gray-800 shadow-sm border-b border-gray-200 dark:border-gray-700 sticky top-0 z-50">
      <div class="mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 max-w-none">
        <div class="flex justify-between items-center h-16">
          <!-- Logo and Brand -->
          <div class="flex items-center">
            <NuxtLink to="/dashboard" class="flex items-center space-x-3">
              <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                <Icon name="heroicons:document-text" class="w-5 h-5 text-white" />
              </div>
              <span class="text-xl font-bold text-gray-900 dark:text-gray-100">CAIV</span>
            </NuxtLink>
          </div>

          <!-- Desktop Navigation Links -->
          <div class="hidden md:flex items-center space-x-8">
            <NuxtLink 
              to="/dashboard" 
              class="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <Icon name="heroicons:home" class="w-4 h-4" />
              <span>Dashboard</span>
            </NuxtLink>
            <NuxtLink 
              to="/resumes" 
              class="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <Icon name="heroicons:document-duplicate" class="w-4 h-4" />
              <span>My Resumes</span>
            </NuxtLink>
            <NuxtLink 
              to="/templates" 
              class="flex items-center space-x-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <Icon name="heroicons:rectangle-stack" class="w-4 h-4" />
              <span>Templates</span>
            </NuxtLink>
          </div>

          <!-- Right side actions -->
          <div class="flex items-center space-x-4">
            <!-- Dark Mode Toggle -->
            <button
              @click="toggle"
              class="p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
              title="Toggle dark mode"
            >
              <Icon name="heroicons:sun" class="w-5 h-5 dark:hidden" />
              <Icon name="heroicons:moon" class="w-5 h-5 hidden dark:block" />
            </button>

            <!-- User Dropdown -->
            <div class="relative">
              <button
                id="user-menu-button"
                @click="toggleUserDropdown"
                class="flex items-center space-x-3 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400"
              >
                <!-- User Avatar -->
                <div class="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-medium text-sm">
                  {{ userInitials }}
                </div>
                <!-- User Name (hidden on mobile) -->
                <span class="hidden sm:block text-gray-700 dark:text-gray-300 font-medium">
                  {{ user?.first_name }} {{ user?.last_name }}
                </span>
                <!-- Dropdown Arrow -->
                <Icon 
                  name="heroicons:chevron-down" 
                  class="w-4 h-4 text-gray-500 dark:text-gray-400 transition-transform"
                  :class="{ 'rotate-180': isUserDropdownOpen }"
                />
              </button>

              <!-- Dropdown Menu -->
              <Transition
                enter-active-class="transition ease-out duration-100"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-75"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="isUserDropdownOpen"
                  id="user-dropdown"
                  class="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg ring-1 ring-black ring-opacity-5 dark:ring-gray-700 z-50"
                >
                  <div class="py-1">
                    <!-- Profile Link -->
                    <button
                      @click="navigateToProfile"
                      class="flex items-center w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
                    >
                      <Icon name="heroicons:user-circle" class="w-4 h-4 mr-3" />
                      Profile 
                    </button>
                    
                    <!-- Divider -->
                    <hr class="border-gray-200 dark:border-gray-700 my-1">
                    
                    <!-- Logout Button -->
                    <button
                      @click="handleLogout"
                      class="flex items-center w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 transition-colors"
                    >
                      <Icon name="heroicons:arrow-right-on-rectangle" class="w-4 h-4 mr-3" />
                      Sign Out
                    </button>
                  </div>
                </div>
              </Transition>
            </div>

            <!-- Mobile menu button -->
            <button
              @click="toggleMobileMenu"
              class="md:hidden p-2 text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              <Icon name="heroicons:bars-3" class="w-5 h-5" v-if="!isMobileMenuOpen" />
              <Icon name="heroicons:x-mark" class="w-5 h-5" v-else />
            </button>
          </div>
        </div>

        <!-- Mobile Navigation Menu -->
        <Transition
          enter-active-class="transition ease-out duration-100"
          enter-from-class="transform opacity-0 scale-95"
          enter-to-class="transform opacity-100 scale-100"
          leave-active-class="transition ease-in duration-75"
          leave-from-class="transform opacity-100 scale-100"
          leave-to-class="transform opacity-0 scale-95"
        >
          <div v-if="isMobileMenuOpen" class="md:hidden border-t border-gray-200 dark:border-gray-700">
            <div class="px-2 pt-2 pb-3 space-y-1 bg-white dark:bg-gray-800">
              <NuxtLink 
                to="/dashboard" 
                @click="isMobileMenuOpen = false"
                class="flex items-center space-x-2 px-3 py-2 rounded-md text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Icon name="heroicons:home" class="w-4 h-4" />
                <span>Dashboard</span>
              </NuxtLink>
              <NuxtLink 
                to="/resumes" 
                @click="isMobileMenuOpen = false"
                class="flex items-center space-x-2 px-3 py-2 rounded-md text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Icon name="heroicons:document-duplicate" class="w-4 h-4" />
                <span>My Resumes</span>
              </NuxtLink>
              <NuxtLink 
                to="/templates" 
                @click="isMobileMenuOpen = false"
                class="flex items-center space-x-2 px-3 py-2 rounded-md text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
              >
                <Icon name="heroicons:rectangle-stack" class="w-4 h-4" />
                <span>Templates</span>
              </NuxtLink>
            </div>
          </div>
        </Transition>
      </div>
    </nav>

    <!-- Main Content -->
    <main>
      <slot />
    </main>
  </div>
</template>