<script setup lang="ts">
defineProps<{
  status: 'indexed' | 'needs_reindex' | 'never_indexed' | 'indexing' | string
  isIndexing?: boolean
}>()
</script>

<template>
  <div class="inline-flex items-center gap-1.5">
    <!-- Indexed -->
    <template v-if="status === 'indexed' && !isIndexing">
      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800">
        <Icon name="mdi:check-circle" class="w-3.5 h-3.5" />
        Indexed
      </span>
    </template>

    <!-- Needs reindex -->
    <template v-else-if="status === 'needs_reindex' && !isIndexing">
      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full bg-amber-50 dark:bg-amber-900/20 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800">
        <Icon name="mdi:alert-circle-outline" class="w-3.5 h-3.5" />
        Needs reindex
      </span>
    </template>

    <!-- Never indexed -->
    <template v-else-if="status === 'never_indexed' && !isIndexing">
      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-gray-700">
        <Icon name="mdi:cloud-outline" class="w-3.5 h-3.5" />
        Not indexed
      </span>
    </template>

    <!-- Currently indexing -->
    <template v-else-if="isIndexing || status === 'indexing'">
      <span class="inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full bg-blue-50 dark:bg-blue-900/20 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800">
        <Icon name="mdi:loading" class="w-3.5 h-3.5 animate-spin" />
        Indexing...
      </span>
    </template>

    <!-- Fallback -->
    <span v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 text-sm font-medium rounded-full bg-gray-50 dark:bg-gray-800 text-gray-500 dark:text-gray-400 border border-gray-200 dark:border-gray-700">
      <Icon name="mdi:help-circle-outline" class="w-3.5 h-3.5" />
      {{ status }}
    </span>
  </div>
</template>
