<script setup lang="ts">
import { ref, computed } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'
import { useToast } from '~/composables/useToast'

const { state, hasResume, refreshPreview } = useCVEditor()
const { success, error } = useToast()

const isRefreshing = ref(false)

const handleRefresh = async () => {
  if (!hasResume.value) return
  isRefreshing.value = true
  try {
    await refreshPreview()
    success('Preview updated', 2000)
  } catch {
    error('Failed to refresh preview', 3000)
  } finally {
    isRefreshing.value = false
  }
}

const showNoResume = computed(() => !hasResume.value)
const showPlaceholder = computed(() => hasResume.value && !state.previewUrl && !state.isGenerating)
const showLoading = computed(() => state.isGenerating)
</script>

<template>
  <div class="flex flex-col h-full bg-gray-100 dark:bg-gray-900">
    <!-- Header with Preview Controls -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex items-center justify-between">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:document-magnifying-glass" class="w-5 h-5" />
        <span>Preview</span>
      </h3>
      <button
        :disabled="isRefreshing || state.isGenerating"
        class="inline-flex items-center space-x-2 px-3 py-1.5 bg-blue-600 text-white text-sm rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        @click="handleRefresh"
      >
        <Icon
          :name="isRefreshing ? 'heroicons:arrow-path' : 'heroicons:arrow-clockwise'"
          :class="{ 'animate-spin': isRefreshing }"
          class="w-4 h-4"
        />
        <span>Refresh</span>
      </button>
    </div>

    <!-- Preview Area -->
    <div class="flex-1 overflow-auto p-4">
      <!-- No Resume -->
      <div v-if="showNoResume" class="flex flex-col items-center justify-center h-full text-center">
        <Icon name="heroicons:document-plus" class="w-16 h-16 text-gray-300 dark:text-gray-600 mb-4" />
        <p class="text-gray-700 dark:text-gray-300 text-lg font-medium mb-2">
          No Resume Loaded
        </p>
        <p class="text-gray-500 dark:text-gray-400 mb-4 max-w-md">
          Create a new resume or select an existing one to start editing.
        </p>
      </div>

      <!-- Placeholder -->
      <div v-else-if="showPlaceholder" class="flex flex-col items-center justify-center h-full text-center">
        <Icon name="heroicons:document-text" class="w-16 h-16 text-gray-300 dark:text-gray-600 mb-4" />
        <p class="text-gray-600 dark:text-gray-400 mb-4">
          Click "Refresh" to generate a PDF preview
        </p>
        <p class="text-sm text-gray-500 dark:text-gray-500">
          The preview will update as you make changes
        </p>
      </div>

      <!-- Loading -->
      <div v-else-if="showLoading" class="flex flex-col items-center justify-center h-full">
        <Icon name="heroicons:arrow-path" class="w-12 h-12 text-blue-400 animate-spin mb-4" />
        <p class="text-gray-600 dark:text-gray-400">Generating preview...</p>
      </div>

      <!-- PDF Preview -->
      <div v-else class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden">
        <iframe
          v-if="state.previewUrl"
          :src="state.previewUrl"
          class="w-full h-full min-h-[600px]"
          title="Resume PDF Preview"
        />
      </div>
    </div>
  </div>
</template>
