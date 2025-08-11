<template>
  <nav class="bg-white/90 dark:bg-gray-900/90 backdrop-blur-xl shadow-lg border-b border-gray-200/50 dark:border-gray-700/50 fixed w-full top-0 z-50 transition-all duration-300">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center space-x-3 cursor-pointer" @click="navigateTo('/')">
          <div class="relative">
            <Icon name="mdi:file-document-edit" class="text-2xl text-blue-600 dark:text-blue-400 transition-transform hover:scale-110" />
            <div class="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          </div>
          <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            CAIV
          </span>
        </div>
        
        <!-- Desktop Navigation -->
        <div class="hidden lg:flex items-center">
          <div class="flex items-center space-x-1">
            <a href="#features" class="flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20">
              <Icon name="mdi:star" class="mr-2" />
              <span class="font-medium">Features</span>
            </a>
            
            <!-- Templates Dropdown -->
            <div class="relative group">
              <button class="flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20 cursor-pointer">
                <Icon name="mdi:view-grid" class="mr-2" />
                <span class="font-medium">Templates</span>
                <Icon name="mdi:chevron-down" class="ml-1 text-sm" />
              </button>
              
              <!-- Dropdown Menu -->
              <div class="absolute left-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-200 z-10">
                <a href="#templates-professional" class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  <Icon name="mdi:briefcase" class="mr-2" />
                  Professional
                </a>
                <a href="#templates-creative" class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  <Icon name="mdi:palette" class="mr-2" />
                  Creative
                </a>
                <a href="#templates-modern" class="flex items-center px-4 py-3 text-gray-700 dark:text-gray-300 hover:bg-blue-50 dark:hover:bg-blue-900/20 hover:text-blue-600 dark:hover:text-blue-400 transition-colors">
                  <Icon name="mdi:trending-up" class="mr-2" />
                  Modern
                </a>
              </div>
            </div>
            
            <a href="#examples" class="flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20">
              <Icon name="mdi:eye" class="mr-2" />
              <span class="font-medium">Examples</span>
            </a>
            
            <a href="#pricing" class="flex items-center px-4 py-2 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20">
              <Icon name="mdi:currency-usd" class="mr-2" />
              <span class="font-medium">Pricing</span>
            </a>
          </div>
        </div>
        
        <!-- Desktop Actions -->
        <div class="hidden lg:flex items-center space-x-3">
          <!-- Dark Mode Toggle -->
          <DarkModeToggle />
          
          <!-- Divider -->
          <div class="h-8 w-px bg-gray-300 dark:bg-gray-600 mx-2"></div>
          
          <!-- Auth Buttons -->
          <div class="flex items-center space-x-2">
            <button
              type="button"
              class="px-4 py-2 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 font-medium transition-colors"
              @click="navigateTo('/login')"
            >
              Sign In
            </button>
            <button
              type="button" 
              class="bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 text-white font-medium px-6 py-2 rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105"
              @click="navigateTo('/register')"
            >
              Get Started
            </button>
          </div>
        </div>

        <!-- Mobile Actions -->
        <div class="lg:hidden flex items-center space-x-2">
          <DarkModeToggle />
          <button
            type="button"
            class="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 p-2 transition-colors"
            @click="toggleMobileMenu"
          >
            <Icon name="mdi:menu" class="text-xl" />
          </button>
        </div>
      </div>
    </div>

    <!-- Mobile Menu Overlay -->
    <div
      v-if="mobileMenuVisible"
      class="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
      @click="mobileMenuVisible = false"
    ></div>

    <!-- Mobile Sidebar Menu -->
    <div
      :class="[
        'fixed top-0 right-0 h-full w-80 bg-white dark:bg-gray-900 shadow-xl transform transition-transform duration-300 z-50 lg:hidden',
        mobileMenuVisible ? 'translate-x-0' : 'translate-x-full'
      ]"
    >
      <!-- Header -->
      <div class="flex items-center justify-between p-6 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center space-x-3">
          <Icon name="mdi:file-document-edit" class="text-2xl text-blue-600 dark:text-blue-400" />
          <span class="text-xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 dark:from-blue-400 dark:to-purple-400 bg-clip-text text-transparent">
            CAIV
          </span>
        </div>
        <button
          @click="mobileMenuVisible = false"
          class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
        >
          <Icon name="mdi:close" class="text-xl" />
        </button>
      </div>

      <!-- Content -->
      <div class="flex flex-col h-full pb-6">
        <!-- Navigation Items -->
        <div class="flex-1 space-y-2 px-4 py-6">
          <div class="space-y-1">
            <h3 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider px-3 py-2">
              Navigation
            </h3>
            <a 
              v-for="item in mobileNavigationItems" 
              :key="item.label"
              :href="item.route" 
              class="flex items-center px-3 py-3 text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-all duration-200"
              @click="mobileMenuVisible = false"
            >
              <Icon :name="item.icon" class="mr-3 text-lg" />
              <span class="font-medium">{{ item.label }}</span>
            </a>
          </div>

          <!-- Divider -->
          <div class="h-px bg-gray-200 dark:bg-gray-700 my-4"></div>

          <!-- Quick Actions -->
          <div class="space-y-3">
            <h3 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider px-3">
              Quick Actions
            </h3>
            <button
              type="button"
              class="w-full px-4 py-3 text-blue-600 dark:text-blue-400 border border-blue-600 dark:border-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/30 rounded-lg transition-colors font-medium"
              @click="navigateAndClose('/login')"
            >
              Sign In
            </button>
            <button
              type="button" 
              class="w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 dark:from-blue-500 dark:to-blue-600 text-white font-medium px-4 py-3 rounded-lg shadow-lg transition-all"
              @click="navigateAndClose('/register')"
            >
              Get Started
            </button>
          </div>

          <!-- Divider -->
          <div class="h-px bg-gray-200 dark:bg-gray-700 my-4"></div>

          <!-- Help & Support -->
          <div class="space-y-1">
            <h3 class="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider px-3 mb-2">
              Support
            </h3>
            <button
              type="button"
              class="w-full flex items-center px-3 py-3 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
            >
              <Icon name="mdi:help-circle" class="mr-3" />
              Help Center
            </button>
            <button
              type="button"
              class="w-full flex items-center px-3 py-3 text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
            >
              <Icon name="mdi:message" class="mr-3" />
              Contact Us
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const mobileMenuVisible = ref(false)

// Mobile Navigation Items (simplified)
const mobileNavigationItems = ref([
  {
    label: 'Features',
    icon: 'mdi:star',
    route: '#features'
  },
  {
    label: 'Templates',
    icon: 'mdi:view-grid',
    route: '#templates'
  },
  {
    label: 'Examples',
    icon: 'mdi:eye',
    route: '#examples'
  },
  {
    label: 'Pricing',
    icon: 'mdi:currency-usd',
    route: '#pricing'
  }
])

const toggleMobileMenu = () => {
  mobileMenuVisible.value = !mobileMenuVisible.value
}

const navigateAndClose = (route: string) => {
  mobileMenuVisible.value = false
  navigateTo(route)
}
</script>

<style scoped>
/* Dropdown hover effect */
.group:hover .group-hover\:opacity-100 {
  opacity: 1;
}

.group:hover .group-hover\:visible {
  visibility: visible;
}

/* Mobile menu slide transition */
.mobile-nav-item:hover {
  background: linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, transparent 100%);
}
</style>