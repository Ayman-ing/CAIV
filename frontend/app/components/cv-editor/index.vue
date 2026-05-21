<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue'
import { useRoute } from 'vue-router'
import CVEditorLayout from './CVEditorLayout.vue'
import { useCVEditor } from '~/composables/useCVEditor'
import { useToast } from '~/composables/useToast'

const route = useRoute()
const { info, error } = useToast()
const { state, loadResume, initEmptyEditor, resetState } = useCVEditor()

onMounted(async () => {
  const resumeUuid = route.query.resume as string
  if (resumeUuid) {
    try {
      await loadResume(resumeUuid)
    } catch (err) {
      console.error('Failed to load CV editor:', err)
      error('Failed to load resume', 5000)
    }
  } else {
    initEmptyEditor()
    info('No resume selected — create a new one or load an existing resume', 3000)
  }
})

onBeforeUnmount(() => {
  if (state.previewUrl) {
    URL.revokeObjectURL(state.previewUrl)
  }
  resetState()
})
</script>

<template>
  <div class="relative w-full h-full min-h-[calc(100vh-4rem)] bg-gray-50 dark:bg-gray-900">
    <!-- Loading State Overlay -->
    <div
      v-if="state.isLoading"
      class="absolute inset-0 z-10 flex items-center justify-center bg-white/80 dark:bg-gray-900/80"
    >
      <div class="text-center">
        <Icon name="heroicons:document-text" class="w-12 h-12 text-gray-400 mx-auto mb-3" />
        <p class="text-gray-600 dark:text-gray-400">Loading resume...</p>
      </div>
    </div>

    <!-- Error State Overlay -->
    <div
      v-else-if="state.error"
      class="absolute inset-0 z-10 flex items-center justify-center bg-white/80 dark:bg-gray-900/80"
    >
      <div class="text-center">
        <Icon name="heroicons:exclamation-triangle" class="w-12 h-12 text-red-400 mx-auto mb-3" />
        <p class="text-red-600 dark:text-red-400 mb-4">{{ state.error }}</p>
        <button
          class="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          @click="navigateTo('/dashboard')"
        >
          Back to Dashboard
        </button>
      </div>
    </div>

    <!-- CV Editor Layout (always visible when not loading/error) -->
    <div v-if="!state.isLoading && !state.error" class="h-full">
      <CVEditorLayout />
    </div>
  </div>
</template>
