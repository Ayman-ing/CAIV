<template>
  <div class="mb-8">
    <div class="flex flex-col md:flex-row md:items-center md:justify-between">
      <div>
        <h1 class="text-3xl font-bold text-text-primary dark:text-text-primary mb-2">
          Welcome back, {{ userName }}! 👋
        </h1>
        <p class="text-text-secondary dark:text-text-secondary text-lg">
          Ready to create your next amazing resume?
        </p>
      </div>
      
      <!-- Quick Stats -->
      <div v-if="showStats" class="mt-4 md:mt-0 flex gap-4">
        <div class="text-center">
          <div class="text-2xl font-bold text-primary-600 dark:text-primary-400">{{ stats.resumes }}</div>
          <div class="text-sm text-text-muted dark:text-text-muted">Resumes</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-green-600 dark:text-green-400">{{ stats.downloads }}</div>
          <div class="text-sm text-text-muted dark:text-text-muted">Downloads</div>
        </div>
        <div class="text-center">
          <div class="text-2xl font-bold text-blue-600 dark:text-blue-400">{{ stats.views }}</div>
          <div class="text-sm text-text-muted dark:text-text-muted">Profile Views</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
interface DashboardHeaderProps {
  userName?: string
  showStats?: boolean
  stats?: {
    resumes: number
    downloads: number
    views: number
  }
}

withDefaults(defineProps<DashboardHeaderProps>(), {
  userName: 'User',
  showStats: true,
  stats: () => ({
    resumes: 0,
    downloads: 0,
    views: 0
  })
})
</script>
