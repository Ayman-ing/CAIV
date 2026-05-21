<script setup lang="ts">
import { ref } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'
import { useToast } from '~/composables/useToast'
import { useProfileStore } from '~/stores/profileStore'

const {
  state,
  hasResume,
  availableTemplates,
  updateTemplate,
  refreshPreview,
  exportPDF,
  saveResume,
  createNewResume
} = useCVEditor()
const { success, error } = useToast()
const { activeProfile, profiles } = useProfileStore()

const isCreatingResume = ref(false)
const isSavingResume = ref(false)
const isExporting = ref(false)

// Handle template change
const handleTemplateChange = (newTemplate: string) => {
  updateTemplate(newTemplate)
}

// Handle refresh preview
const handleRefreshPreview = async () => {
  try {
    await refreshPreview()
  } catch {
    error('Failed to refresh preview', 3000)
  }
}

// Handle create resume
const handleCreateResume = async () => {
  isCreatingResume.value = true
  try {
    const profileId = activeProfile.value?.uuid || profiles.value[0]?.uuid
    if (!profileId) {
      error('No profile available. Please create a profile first.', 5000)
      return
    }
    await createNewResume(profileId, state.selectedTemplate, 'My Resume')
    success('Resume created successfully', 3000)
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to create resume'
    error(message, 3000)
  } finally {
    isCreatingResume.value = false
  }
}

// Handle save resume
const handleSaveResume = async () => {
  isSavingResume.value = true
  try {
    await saveResume()
    success('Resume saved successfully', 3000)
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to save resume'
    error(message, 3000)
  } finally {
    isSavingResume.value = false
  }
}

// Handle export PDF
const handleExportPDF = async () => {
  isExporting.value = true
  try {
    await exportPDF()
  } catch (err) {
    const message = err instanceof Error ? err.message : 'Failed to export PDF'
    error(message, 3000)
  } finally {
    isExporting.value = false
  }
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:cog-6-tooth" class="w-5 h-5" />
        <span>Export & Settings</span>
      </h3>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- Template Selector -->
      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Icon name="heroicons:document-text" class="w-4 h-4 inline mr-1" />
          Template
        </label>
        <select
          :value="state.selectedTemplate"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          @change="handleTemplateChange(($event.target as HTMLSelectElement).value)"
        >
          <option v-for="template in availableTemplates" :key="template.value" :value="template.value">
            {{ template.label }}
          </option>
        </select>
      </div>

      <!-- Resume Title (if editable) -->
      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Icon name="heroicons:pencil" class="w-4 h-4 inline mr-1" />
          Resume Title
        </label>
        <input
          type="text"
          :value="state.currentResume?.title || 'Untitled Resume'"
          placeholder="Enter resume title"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
          readonly
        >
      </div>

      <!-- Summary Stats -->
      <div v-if="hasResume" class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <h4 class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider mb-3">
          Resume Stats
        </h4>
        <div class="space-y-2">
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-600 dark:text-gray-400">Total Sections</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100">{{ state.components.length }}</span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-600 dark:text-gray-400">Included</span>
            <span class="font-semibold text-blue-600 dark:text-blue-400">
              {{ state.components.filter(c => c.is_included).length }}
            </span>
          </div>
          <div class="flex justify-between items-center text-sm">
            <span class="text-gray-600 dark:text-gray-400">Template</span>
            <span class="font-semibold text-gray-900 dark:text-gray-100 capitalize">
              {{ state.selectedTemplate.toLowerCase() }}
            </span>
          </div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="px-4 py-4 space-y-3">
        <!-- Create Resume Button (when no resume loaded) -->
        <button
          v-if="!hasResume"
          :disabled="isCreatingResume"
          class="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          @click="handleCreateResume"
        >
          <Icon
            :name="isCreatingResume ? 'heroicons:arrow-path' : 'heroicons:plus-circle'"
            :class="isCreatingResume ? 'animate-spin' : ''"
            class="w-4 h-4"
          />
          <span>{{ isCreatingResume ? 'Creating...' : 'Create Resume' }}</span>
        </button>

        <!-- Refresh Preview Button (when resume loaded) -->
        <button
          v-if="hasResume"
          :disabled="state.isGenerating"
          class="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          @click="handleRefreshPreview"
        >
          <Icon
            :name="state.isGenerating ? 'heroicons:arrow-path' : 'heroicons:arrow-clockwise'"
            :class="state.isGenerating ? 'animate-spin' : ''"
            class="w-4 h-4"
          />
          <span>{{ state.isGenerating ? 'Generating...' : 'Refresh Preview' }}</span>
        </button>

        <!-- Save Resume Button -->
        <button
          v-if="hasResume"
          :disabled="isSavingResume || state.isSaving"
          class="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 bg-green-600 text-white text-sm font-medium rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          @click="handleSaveResume"
        >
          <Icon
            :name="isSavingResume ? 'heroicons:arrow-path' : 'heroicons:check'"
            :class="isSavingResume ? 'animate-spin' : ''"
            class="w-4 h-4"
          />
          <span>{{ isSavingResume ? 'Saving...' : 'Save Resume' }}</span>
        </button>

        <!-- Export PDF Button -->
        <button
          v-if="hasResume"
          :disabled="isExporting || !state.previewUrl"
          class="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          @click="handleExportPDF"
        >
          <Icon
            :name="isExporting ? 'heroicons:arrow-path' : 'heroicons:arrow-down-tray'"
            :class="isExporting ? 'animate-spin' : ''"
            class="w-4 h-4"
          />
          <span>{{ isExporting ? 'Exporting...' : 'Export as PDF' }}</span>
        </button>
      </div>

      <!-- Help Text -->
      <div class="px-4 py-4 text-xs text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/30 mx-2 rounded-lg">
        <p class="font-medium mb-1">Tips:</p>
        <ul class="list-disc list-inside space-y-1">
          <li>Click "Refresh Preview" after making changes</li>
          <li>Use the left sidebar to include/exclude sections</li>
          <li>Select a template to change the resume layout</li>
          <li>Click "Export as PDF" to download your resume</li>
        </ul>
      </div>
    </div>
  </div>
</template>
