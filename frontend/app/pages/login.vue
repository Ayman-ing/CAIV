<script setup lang="ts">
definePageMeta({
  middleware: 'guest'
})
</script>
<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Navigation -->
    <SectionsNavigation />
    
    <!-- Split Screen Layout -->
    <div class="flex min-h-screen pt-16">
      <!-- Left Side - Form -->
      <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900">
        <AuthLoginForm 
          @switch-to-register="navigateTo('/register')"
        />
      </div>

      <!-- Right Side - Background/Marketing -->
      <div class="hidden lg:block flex-1 relative bg-gradient-to-br from-blue-600 to-purple-700">
        <div class="absolute inset-0 bg-black/20"></div>
        <div class="relative flex flex-col justify-center h-full px-12">
          <div class="space-y-6 text-white">
            <h2 class="text-4xl font-bold">Welcome back to AI Resume Builder</h2>
            <p class="text-xl text-blue-100">
              Continue building your professional future with our advanced AI tools.
            </p>
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Resume analytics and insights</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Job matching recommendations</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Career progression tracking</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Interview preparation tools</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


