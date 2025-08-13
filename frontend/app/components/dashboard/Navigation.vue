<template>
  <nav class="bg-white dark:bg-surface shadow-sm border-b border-border dark:border-border">
    <div class="container mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo -->
        <div class="flex items-center space-x-3">
          <Icon name="lucide:file-text" class="text-2xl text-primary-600 dark:text-primary-400" />
          <span class="text-xl font-bold text-text-primary dark:text-text-primary">AI Resume Builder</span>
        </div>
        
        <!-- User Menu -->
        <div class="flex items-center space-x-4">
          <DarkModeToggle />
          
          <Button
            variant="ghost"
            icon="lucide:user"
            size="sm"
            @click="$emit('profile')"
          >
            Profile
          </Button>
          
          <Button
            variant="ghost"
            icon="lucide:log-out"
            size="sm"
            @click="$emit('logout')"
          >
            Logout
          </Button>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup lang="ts">
interface DashboardNavigationEmits {
  (e: 'profile'): void
  (e: 'logout'): void
}

defineEmits<DashboardNavigationEmits>()
</script>
