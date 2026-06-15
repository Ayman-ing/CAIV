<script setup lang="ts">
import { ref } from 'vue'
import { useCVEditor } from '~/composables/useCVEditor'
import { useToast } from '~/composables/useToast'

const {
  state,
  updateBasicInfo,
  addLink,
  removeLink,
  exportPDF,
  updateLayout,
  updatePageMargin,
} = useCVEditor()
const { error } = useToast()

const isExporting = ref(false)

const newLinkUrl = ref('')
const newLinkLabel = ref('')
const showAddLink = ref(false)

const handleExportPDF = async () => {
  isExporting.value = true
  try {
    await exportPDF()
  } catch {
    error('Failed to export PDF', 3000)
  } finally {
    isExporting.value = false
  }
}

const handleAddLink = () => {
  if (!newLinkUrl.value.trim()) return
  addLink({
    uuid: crypto.randomUUID(),
    label: newLinkLabel.value.trim() || newLinkUrl.value,
    url: newLinkUrl.value.trim(),
    platform: 'other',
    is_visible: true,
  })
  newLinkUrl.value = ''
  newLinkLabel.value = ''
  showAddLink.value = false
}
</script>

<template>
  <div class="flex flex-col h-full">
    <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700 bg-gray-50 dark:bg-gray-700/50">
      <h3 class="font-semibold text-gray-900 dark:text-gray-100 flex items-center space-x-2">
        <Icon name="heroicons:cog-6-tooth" class="w-5 h-5" />
        <span>Settings</span>
      </h3>
    </div>

    <div class="flex-1 overflow-y-auto">
      <div class="px-4 py-3 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between text-sm">
          <span class="text-gray-600 dark:text-gray-400">Template</span>
          <span class="font-medium text-gray-900 dark:text-gray-100">Classic Canadian</span>
        </div>
      </div>

      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          <Icon name="heroicons:user" class="w-4 h-4 inline mr-1" />
          Basic Info
        </label>
        <div class="space-y-2">
          <input
            :value="state.profileData.basicInfo.name"
            placeholder="Full Name"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="updateBasicInfo('name', ($event.target as HTMLInputElement).value)"
          >
          <input
            :value="state.profileData.basicInfo.email"
            placeholder="Email"
            type="email"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="updateBasicInfo('email', ($event.target as HTMLInputElement).value)"
          >
          <input
            :value="state.profileData.basicInfo.phone"
            placeholder="Phone"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="updateBasicInfo('phone', ($event.target as HTMLInputElement).value)"
          >
          <input
            :value="state.profileData.basicInfo.location"
            placeholder="Location"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
            @input="updateBasicInfo('location', ($event.target as HTMLInputElement).value)"
          >
        </div>
      </div>

      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <div class="flex items-center justify-between mb-2">
          <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
            <Icon name="heroicons:link" class="w-4 h-4 inline mr-1" />
            Links
          </label>
          <button
            class="text-xs text-blue-600 dark:text-blue-400 hover:underline"
            @click="showAddLink = !showAddLink"
          >
            + Add
          </button>
        </div>
        <div v-if="showAddLink" class="space-y-2 mb-3 p-2 bg-gray-50 dark:bg-gray-700/30 rounded-lg">
          <input
            v-model="newLinkLabel"
            placeholder="Label (e.g. Portfolio)"
            class="w-full px-2 py-1.5 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <input
            v-model="newLinkUrl"
            placeholder="URL (e.g. https://...)"
            class="w-full px-2 py-1.5 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
          <div class="flex space-x-2">
            <button
              class="px-2 py-1 text-xs bg-blue-600 text-white rounded hover:bg-blue-700"
              @click="handleAddLink"
            >
              Add
            </button>
            <button
              class="px-2 py-1 text-xs text-gray-600 dark:text-gray-400 hover:underline"
              @click="showAddLink = false"
            >
              Cancel
            </button>
          </div>
        </div>
        <div class="space-y-1">
          <div
            v-for="link in state.profileData.links"
            :key="link.uuid"
            class="flex items-center justify-between text-sm py-1"
          >
            <div class="flex items-center space-x-2 min-w-0 flex-1">
              <span class="text-gray-600 dark:text-gray-400 text-xs truncate">
                {{ link.label }}
              </span>
              <span class="text-gray-400 text-xs truncate hidden sm:inline">
                {{ link.url }}
              </span>
            </div>
            <button
              class="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 flex-shrink-0"
              title="Remove link"
              @click="removeLink(link.uuid)"
            >
              <Icon name="heroicons:x-mark" class="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700 space-y-3">
        <label class="block text-sm font-medium text-gray-700 dark:text-gray-300">
          <Icon name="heroicons:document-text" class="w-4 h-4 inline mr-1" />
          Layout
        </label>

        <div>
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Font Size</span>
            <span>{{ state.layout.fontSize }}px</span>
          </div>
          <input
            type="range"
            min="8"
            max="14"
            step="0.5"
            :value="state.layout.fontSize"
            class="w-full accent-blue-600"
            @input="updateLayout('fontSize', parseFloat(($event.target as HTMLInputElement).value))"
          >
        </div>

        <div>
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Line Height</span>
            <span>{{ state.layout.lineHeight.toFixed(1) }}</span>
          </div>
          <input
            type="range"
            min="1.0"
            max="2.0"
            step="0.1"
            :value="state.layout.lineHeight"
            class="w-full accent-blue-600"
            @input="updateLayout('lineHeight', parseFloat(($event.target as HTMLInputElement).value))"
          >
        </div>

        <div>
          <div class="flex justify-between text-xs text-gray-500 mb-1">
            <span>Section Spacing</span>
            <span>{{ state.layout.sectionSpacing }}px</span>
          </div>
          <input
            type="range"
            min="4"
            max="32"
            step="1"
            :value="state.layout.sectionSpacing"
            class="w-full accent-blue-600"
            @input="updateLayout('sectionSpacing', parseFloat(($event.target as HTMLInputElement).value))"
          >
        </div>

        <div>
          <span class="text-xs text-gray-500 block mb-1">Page Margins</span>
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="text-[10px] text-gray-400 block">Top</label>
              <input
                type="number"
                min="10"
                max="80"
                :value="state.layout.pageMargins.top"
                class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                @input="updatePageMargin('top', parseInt(($event.target as HTMLInputElement).value) || 10)"
              >
            </div>
            <div>
              <label class="text-[10px] text-gray-400 block">Bottom</label>
              <input
                type="number"
                min="10"
                max="80"
                :value="state.layout.pageMargins.bottom"
                class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                @input="updatePageMargin('bottom', parseInt(($event.target as HTMLInputElement).value) || 10)"
              >
            </div>
            <div>
              <label class="text-[10px] text-gray-400 block">Left</label>
              <input
                type="number"
                min="10"
                max="80"
                :value="state.layout.pageMargins.left"
                class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                @input="updatePageMargin('left', parseInt(($event.target as HTMLInputElement).value) || 10)"
              >
            </div>
            <div>
              <label class="text-[10px] text-gray-400 block">Right</label>
              <input
                type="number"
                min="10"
                max="80"
                :value="state.layout.pageMargins.right"
                class="w-full px-2 py-1 border border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 text-xs focus:outline-none focus:ring-2 focus:ring-blue-500"
                @input="updatePageMargin('right', parseInt(($event.target as HTMLInputElement).value) || 10)"
              >
            </div>
          </div>
        </div>
      </div>

      <div class="px-4 py-4 border-b border-gray-200 dark:border-gray-700">
        <button
          class="w-full inline-flex items-center justify-center space-x-2 px-4 py-2.5 bg-purple-600 text-white text-sm font-medium rounded-lg hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          :disabled="isExporting"
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

      <div class="px-4 py-4 text-xs text-gray-600 dark:text-gray-400 bg-gray-50 dark:bg-gray-700/30 mx-2 rounded-lg mb-4">
        <p class="font-medium mb-1">Tips:</p>
        <ul class="list-disc list-inside space-y-1">
          <li>Edit fields above — changes appear instantly on the paper</li>
          <li>Use the left sidebar to reorder sections</li>
          <li>Collapse sections you're not working on</li>
          <li>Save drafts frequently to avoid losing work</li>
        </ul>
      </div>
    </div>
  </div>
</template>
