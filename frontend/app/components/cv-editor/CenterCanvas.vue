<script setup lang="ts">
import { ref } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'
import { useToast } from '~/composables/useToast'
import PaperPreview from './PaperPreview.vue'
import SaveDraftModal from './SaveDraftModal.vue'

const { state, saveCurrentDraft } = useCVEditor()
const { success, error } = useToast()

const showSaveModal = ref(false)
const isSaving = ref(false)

const handleSave = async () => {
  if (state.isSaving) return

  if (!state.draftUuid) {
    showSaveModal.value = true
    return
  }

  isSaving.value = true
  try {
    await saveCurrentDraft()
    success('Draft saved', 2000)
  } catch {
    error('Failed to save draft', 3000)
  } finally {
    isSaving.value = false
  }
}

const handleSaveWithTitle = async (title: string) => {
  showSaveModal.value = false
  isSaving.value = true
  try {
    await saveCurrentDraft(title)
    success('Draft saved', 2000)
  } catch {
    error('Failed to save draft', 3000)
  } finally {
    isSaving.value = false
  }
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 flex items-center justify-between">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:document-magnifying-glass" class="w-5 h-5" />
        <span>Preview</span>
      </h3>
      <div class="flex items-center space-x-2">
        <span v-if="state.draftTitle" class="text-xs text-gray-500 dark:text-gray-400 mr-2 truncate max-w-[120px]">
          {{ state.draftTitle }}
        </span>
        <button
          :disabled="isSaving || state.isSaving"
          class="inline-flex items-center space-x-1.5 px-3 py-1.5 bg-blue-600 text-white text-xs font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          @click="handleSave"
        >
          <Icon
            :name="isSaving ? 'heroicons:arrow-path' : 'heroicons:document'"
            :class="isSaving ? 'animate-spin' : ''"
            class="w-3.5 h-3.5"
          />
          <span>{{ isSaving ? 'Saving...' : 'Save Draft' }}</span>
        </button>
      </div>
    </div>
    <div class="flex-1 overflow-hidden">
      <PaperPreview />
    </div>
    <SaveDraftModal
      v-if="showSaveModal"
      :initial-title="state.draftTitle || 'My Resume'"
      @confirm="handleSaveWithTitle"
      @cancel="showSaveModal = false"
    />
  </div>
</template>
