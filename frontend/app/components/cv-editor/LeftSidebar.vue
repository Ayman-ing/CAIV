<script setup lang="ts">
import { ref } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'

const {
  state,
  includedComponents,
  excludedComponents,
  toggleComponent,
  reorderComponents
} = useCVEditor()

const componentTypeLabels: Record<string, string> = {
  'professional_summary': 'Professional Summary',
  'work_experience': 'Work Experience',
  'education': 'Education',
  'skills': 'Skills',
  'projects': 'Projects',
  'certificates': 'Certificates',
  'languages': 'Languages',
  'custom_sections': 'Custom Sections',
  'profile_links': 'Profile Links'
}

// Drag and drop state
const draggedComponent = ref<string | null>(null)

// Handle drag start
const handleDragStart = (e: DragEvent, componentUuid: string) => {
  draggedComponent.value = componentUuid
  if (e.dataTransfer) {
    e.dataTransfer.effectAllowed = 'move'
  }
}

// Handle drag over
const handleDragOver = (e: DragEvent) => {
  e.preventDefault()
  if (e.dataTransfer) {
    e.dataTransfer.dropEffect = 'move'
  }
}

// Handle drop
const handleDrop = (e: DragEvent, targetUuid: string) => {
  e.preventDefault()
  if (draggedComponent.value && draggedComponent.value !== targetUuid) {
    const draggedIdx = includedComponents.value.findIndex(c => c.uuid === draggedComponent.value)
    const targetIdx = includedComponents.value.findIndex(c => c.uuid === targetUuid)

    if (draggedIdx !== -1 && targetIdx !== -1) {
      const newOrder = [...includedComponents.value]
      const movedComponent = newOrder.splice(draggedIdx, 1)[0]
      if (movedComponent) {
        newOrder.splice(targetIdx, 0, movedComponent)
        reorderComponents(newOrder)
      }
    }
  }
  draggedComponent.value = null
}

const getTypeLabel = (type: string): string => {
  return componentTypeLabels[type] || type.replace(/_/g, ' ').toUpperCase()
}

const getTypeIcon = (type: string): string => {
  const iconMap: Record<string, string> = {
    'professional_summary': 'heroicons:document-text',
    'work_experience': 'heroicons:briefcase',
    'education': 'heroicons:academic-cap',
    'skills': 'heroicons:sparkles',
    'projects': 'heroicons:folder',
    'certificates': 'heroicons:trophy',
    'languages': 'heroicons:chat-bubble-left-right',
    'custom_sections': 'heroicons:rectangle-stack',
    'profile_links': 'heroicons:link'
  }
  return iconMap[type] || 'heroicons:document'
}
</script>

<template>
  <div class="flex flex-col h-full">
    <!-- Header -->
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:rectangle-stack" class="w-5 h-5" />
        <span>Resume Sections</span>
      </h3>
      <p class="text-xs text-gray-600 dark:text-gray-400 mt-1">
        {{ includedComponents.length }} included · {{ excludedComponents.length }} available
      </p>
    </div>

    <!-- Content -->
    <div class="flex-1 overflow-y-auto">
      <!-- Included Components (Draggable) -->
      <div v-if="includedComponents.length > 0" class="border-b border-gray-200 dark:border-gray-700">
        <div class="px-4 py-2 bg-blue-50 dark:bg-blue-900/20 border-b border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-blue-900 dark:text-blue-100 uppercase tracking-wider">
            Included Sections
          </h4>
        </div>
        <div class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="component in includedComponents"
            :key="component.uuid"
            draggable
            class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 cursor-move transition-colors group flex items-center justify-between"
            @dragstart="handleDragStart($event, component.uuid)"
            @dragover="handleDragOver"
            @drop="handleDrop($event, component.uuid)"
          >
            <div class="flex items-center space-x-2 flex-1 min-w-0">
              <Icon name="heroicons:bars-3" class="w-4 h-4 text-gray-400 flex-shrink-0" />
              <Icon :name="getTypeIcon(component.component_type)" class="w-4 h-4 text-blue-600 dark:text-blue-400 flex-shrink-0" />
              <span class="text-sm text-gray-700 dark:text-gray-300 truncate">
                {{ getTypeLabel(component.component_type) }}
              </span>
            </div>
            <button
              class="ml-2 p-1 text-gray-400 hover:text-red-600 dark:text-gray-500 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-all"
              title="Exclude section"
              @click="toggleComponent(component.uuid)"
            >
              <Icon name="heroicons:x-mark" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Excluded Components -->
      <div v-if="excludedComponents.length > 0">
        <div class="px-4 py-2 bg-gray-100 dark:bg-gray-700 border-b border-gray-200 dark:border-gray-700">
          <h4 class="text-xs font-semibold text-gray-700 dark:text-gray-300 uppercase tracking-wider">
            Available Sections
          </h4>
        </div>
        <div class="divide-y divide-gray-200 dark:divide-gray-700">
          <div
            v-for="component in excludedComponents"
            :key="component.uuid"
            class="px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors group flex items-center justify-between opacity-60 hover:opacity-100"
          >
            <div class="flex items-center space-x-2">
              <Icon :name="getTypeIcon(component.component_type)" class="w-4 h-4 text-gray-600 dark:text-gray-400" />
              <span class="text-sm text-gray-600 dark:text-gray-400">
                {{ getTypeLabel(component.component_type) }}
              </span>
            </div>
            <button
              class="ml-2 p-1 text-gray-400 hover:text-green-600 dark:text-gray-500 dark:hover:text-green-400 opacity-0 group-hover:opacity-100 transition-all"
              title="Include section"
              @click="toggleComponent(component.uuid)"
            >
              <Icon name="heroicons:plus" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-if="state.components.length === 0" class="flex flex-col items-center justify-center h-full text-center p-4">
        <Icon name="heroicons:document-text" class="w-12 h-12 text-gray-300 dark:text-gray-600 mb-2" />
        <p class="text-gray-600 dark:text-gray-400 text-sm">
          No sections available yet
        </p>
      </div>
    </div>
  </div>
</template>
