<script setup lang="ts">
// filepath: frontend/app/components/profile/links/LinksSection.vue
import { ref } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'

interface Link {
  id: string
  platform: string
  url: string
  customPlatform?: string
}

// Links Data
const links = ref<Link[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingLink = ref<Link | null>(null)

// Form state
const formData = ref<Link>({
  id: '',
  platform: 'linkedin',
  url: '',
  customPlatform: ''
})

// Platform options
const platformOptions = [
  { value: 'linkedin', label: 'LinkedIn', icon: 'mdi:linkedin' },
  { value: 'github', label: 'GitHub', icon: 'mdi:github' },
  { value: 'website', label: 'Personal Website', icon: 'mdi:web' },
  { value: 'portfolio', label: 'Portfolio', icon: 'mdi:briefcase' },
  { value: 'twitter', label: 'Twitter', icon: 'mdi:twitter' },
  { value: 'instagram', label: 'Instagram', icon: 'mdi:instagram' },
  { value: 'facebook', label: 'Facebook', icon: 'mdi:facebook' },
  { value: 'youtube', label: 'YouTube', icon: 'mdi:youtube' },
  { value: 'other', label: 'Other', icon: 'mdi:link' }
]

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingLink.value = null
  formData.value = {
    id: Date.now().toString(),
    platform: 'linkedin',
    url: '',
    customPlatform: ''
  }
  isModalOpen.value = true
}

const openEditModal = (link: Link) => {
  isEditing.value = true
  editingLink.value = link
  formData.value = { ...link }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingLink.value) {
    // Update existing link
    const index = links.value.findIndex(l => l.id === editingLink.value!.id)
    if (index !== -1) {
      links.value[index] = { ...formData.value }
    }
  } else {
    // Add new link
    links.value.push({ ...formData.value })
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingLink.value = null
  formData.value = {
    id: '',
    platform: 'linkedin',
    url: '',
    customPlatform: ''
  }
}

const removeLink = (id: string) => {
  links.value = links.value.filter(link => link.id !== id)
}

const getPlatformIcon = (platform: string) => {
  const option = platformOptions.find(opt => opt.value === platform)
  return option?.icon || 'mdi:link'
}

const getPlatformLabel = (platform: string, customPlatform?: string) => {
  if (platform === 'other' && customPlatform) {
    return customPlatform
  }
  const option = platformOptions.find(opt => opt.value === platform)
  return option?.label || 'Unknown'
}

const isFormValid = computed(() => {
  return formData.value.url.trim() !== '' && 
    (formData.value.platform !== 'other' || formData.value.customPlatform?.trim() !== '')
})
</script>

<template>
  <CollapsibleSection
    title="Links & Social Media"
    description="Your online presence and professional profiles"
    icon="mdi:link-variant"
    icon-color="text-purple-600 dark:text-purple-400"
    icon-bg-color="bg-purple-100 dark:bg-purple-900/30"
    button-color="bg-purple-600 dark:bg-purple-500 hover:bg-purple-700 dark:hover:bg-purple-600"
    :is-expanded="isExpanded"
    :is-empty="links.length === 0"
    empty-message="No links added yet"
    add-button-text="Add Links"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode - Show existing links -->
    <div v-if="links.length > 0" class="space-y-3">
      <div v-for="link in links" :key="link.id" class="flex items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-300 dark:border-gray-600 group hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
        <Icon :name="getPlatformIcon(link.platform)" class="w-6 h-6 text-purple-600 dark:text-purple-400 mr-3 flex-shrink-0" />
        
        <div class="flex-1 min-w-0">
          <div class="flex items-center space-x-2 mb-1">
            <span class="font-medium text-gray-900 dark:text-gray-100">{{ getPlatformLabel(link.platform, link.customPlatform) }}</span>
            <Icon name="mdi:open-in-new" class="w-4 h-4 text-gray-400 dark:text-gray-500" />
          </div>
          <a 
            :href="link.url" 
            target="_blank" 
            rel="noopener noreferrer" 
            class="text-sm text-blue-600 dark:text-blue-400 hover:underline break-all block"
          >
            {{ link.url }}
          </a>
        </div>

        <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button
            @click="openEditModal(link)"
            class="p-2 text-gray-500 hover:text-purple-600 dark:hover:text-purple-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
            title="Edit link"
          >
            <Icon name="mdi:pencil" class="w-4 h-4" />
          </button>
          
          <button
            @click="removeLink(link.id)"
            class="p-2 text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
            title="Remove link"
          >
            <Icon name="mdi:trash-can" class="w-4 h-4" />
          </button>
        </div>
      </div>

      <div class="flex justify-center pt-3 border-t border-gray-200 dark:border-gray-700">
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Another Link
        </button>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Link' : 'Add New Link'"
    size="lg"
    @close="closeModal"
  >
    <div class="space-y-4">
      <!-- Platform Selection -->
      <div>
        <label for="platform" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Platform *
        </label>
        <select
          id="platform"
          v-model="formData.platform"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        >
          <option v-for="option in platformOptions" :key="option.value" :value="option.value">
            <Icon :name="option.icon" class="w-4 h-4 mr-2" />
            {{ option.label }}
          </option>
        </select>
      </div>

      <!-- Custom Platform Input (shown when "Other" is selected) -->
      <div v-if="formData.platform === 'other'">
        <label for="customPlatform" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Platform Name *
        </label>
        <input
          id="customPlatform"
          v-model="formData.customPlatform"
          type="text"
          placeholder="Enter platform name (e.g., Behance, Dribbble)"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <!-- URL Input -->
      <div>
        <label for="url" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          URL *
        </label>
        <input
          id="url"
          v-model="formData.url"
          type="url"
          placeholder="https://..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Enter the complete URL including https://
        </p>
      </div>

      <!-- Preview -->
      <div v-if="formData.url" class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
        <p class="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Preview:</p>
        <div class="flex items-center space-x-3">
          <Icon :name="getPlatformIcon(formData.platform)" class="w-5 h-5 text-purple-600 dark:text-purple-400" />
          <div>
            <div class="font-medium text-gray-900 dark:text-gray-100">
              {{ getPlatformLabel(formData.platform, formData.customPlatform) }}
            </div>
            <div class="text-sm text-blue-600 dark:text-blue-400 break-all">
              {{ formData.url }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        @click="closeModal"
        class="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors"
      >
        Cancel
      </button>
      
      <button
        @click="handleSave"
        :disabled="!isFormValid"
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Link' : 'Add Link' }}
      </button>
    </template>
  </Modal>
</template>