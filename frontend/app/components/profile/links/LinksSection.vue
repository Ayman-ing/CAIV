<script setup lang="ts">
// filepath: frontend/app/components/profile/links/LinksSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { ProfileLink, LinkFormData, LinkDisplay } from './types'
import { LINK_TYPES } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'
import { useToast } from '~/composables/useToast'
import { useUrlValidator } from '~/composables/useUrlValidator'
import { useFormValidation } from '~/composables/useFormValidation'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()
const { isValidUrl, getUrlErrorMessage, normalizeUrl } = useUrlValidator()
const { validateLength } = useFormValidation()

// Form validation errors
const urlValidationError = ref<string | null>(null)
const labelValidationError = ref<string | null>(null)

// Links Data
const links = ref<ProfileLink[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingLink = ref<ProfileLink | null>(null)
const isDeleteModalOpen = ref(false)
const linkToDelete = ref<ProfileLink | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<LinkFormData>({
  label: '',
  url: '',
  platform: 'linkedin',
  is_visible: true
})

onMounted(async () => {
  await fetchLinks()
})

const fetchLinks = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllProfileLinks(activeProfile.value.uuid)
    links.value = data
  } catch (error) {
    console.error('Failed to fetch links:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingLink.value = null
  formData.value = {
    label: '',
    url: '',
    platform: 'linkedin',
    is_visible: true
  }
  isModalOpen.value = true
}

const openEditModal = (link: ProfileLink) => {
  isEditing.value = true
  editingLink.value = link
  formData.value = {
    label: link.label,
    url: link.url,
    platform: link.platform,
    is_visible: link.is_visible
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  // Validate label length
  const labelError = validateLength(formData.value.label, 1, 200)
  if (labelError && formData.value.label.trim()) {
    labelValidationError.value = labelError
    return
  }
  labelValidationError.value = null
  
  // Validate URL
  const urlError = getUrlErrorMessage(formData.value.url)
  if (urlError) {
    urlValidationError.value = urlError
    return
  }
  urlValidationError.value = null
  
  const payload: Omit<ProfileLink, 'uuid'> = {
    label: formData.value.label.trim() || formData.value.platform,
    url: normalizeUrl(formData.value.url),
    platform: formData.value.platform,
    is_visible: formData.value.is_visible
  }

  try {
    if (isEditing.value && editingLink.value) {
      await profileSectionsService.updateProfileLink(
        activeProfile.value.uuid,
        editingLink.value.uuid,
        payload
      )
      success('Link updated successfully!')
    } else {
      await profileSectionsService.createProfileLink(activeProfile.value.uuid, payload)
      success('Link added successfully!')
    }
    await fetchLinks()
    closeModal()
  } catch (err) {
    error(`Failed to save link: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingLink.value = null
}

const openDeleteModal = (link: ProfileLink) => {
  linkToDelete.value = link
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  linkToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !linkToDelete.value) return
  isDeleting.value = true
  try {
    await profileSectionsService.deleteProfileLink(activeProfile.value.uuid, linkToDelete.value.uuid)
    await fetchLinks()
    closeDeleteModal()
    success('Link deleted successfully!')
  } catch (err) {
    error(`Failed to delete link: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  const hasUrl = formData.value.url.trim() !== ''
  const urlIsValid = hasUrl ? isValidUrl(formData.value.url) : true
  return hasUrl && urlIsValid
})

const hasLinks = computed(() => links.value.length > 0)

const displayLinks = computed<LinkDisplay[]>(() => {
  return links.value.map(link => {
    const config = LINK_TYPES.find(t => t.value === link.platform) || LINK_TYPES[LINK_TYPES.length - 1]
    return {
      ...link,
      icon: config?.icon || 'mdi:link-variant',
      domain: '',
      isValidUrl: true,
      isProfessional: config?.isProfessional || false,
      displayUrl: link.url.replace(/^https?:\/\//, '').replace(/\/$/, '')
    } as LinkDisplay
  })
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
    :is-empty="!isLoading && !hasLinks"
    empty-message="No links added yet"
    add-button-text="Add Links"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-purple-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasLinks" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-purple-50 dark:bg-purple-900/20 rounded-lg border border-purple-200 dark:border-purple-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:link-variant" class="w-5 h-5 text-purple-600 dark:text-purple-400" />
            <div>
              <p class="text-sm font-medium text-purple-700 dark:text-purple-300">Links & Social Media</p>
              <p class="text-xs text-purple-600 dark:text-purple-400">{{ displayLinks.length }} link{{ displayLinks.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-purple-600 hover:bg-purple-700 dark:bg-purple-500 dark:hover:bg-purple-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Link
        </button>
      </div>

      <!-- Links List -->
      <div class="space-y-3">
        <div v-for="link in displayLinks" :key="link.uuid" class="flex items-center p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-300 dark:border-gray-600 group hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
        <Icon :name="link.icon" class="w-6 h-6 text-purple-600 dark:text-purple-400 mr-3 flex-shrink-0" />
        
        <div class="flex-1 min-w-0">
          <div class="flex items-center space-x-2 mb-1">
            <span class="font-medium text-gray-900 dark:text-gray-100">{{ link.label }}</span>
            <Icon v-if="!link.is_visible" name="mdi:eye-off" class="w-4 h-4 text-gray-400" />
          </div>
          <a :href="link.url" target="_blank" rel="noopener noreferrer" class="text-sm text-blue-600 dark:text-blue-400 hover:underline break-all block">
            {{ link.displayUrl }}
          </a>
        </div>

        <div class="flex items-center space-x-2 opacity-0 group-hover:opacity-100 transition-opacity">
          <button @click="openEditModal(link)" class="p-2 text-gray-500 hover:text-purple-600 rounded-md transition-colors">
            <Icon name="mdi:pencil" class="w-4 h-4" />
          </button>
          <button @click="openDeleteModal(link)" class="p-2 text-gray-500 hover:text-red-600 rounded-md transition-colors">
            <Icon name="mdi:trash-can" class="w-4 h-4" />
          </button>
        </div>
      </div>
      </div>

 
    </div>
  </CollapsibleSection>
    
  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Link"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Link?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ linkToDelete?.label }}</span>? This action cannot be undone.
          </p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeDeleteModal"
          :disabled="isDeleting"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          @click="confirmDelete"
          :disabled="isDeleting"
          class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isDeleting ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </template>
  </Modal>
  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Link' : 'Add New Link'"
    size="lg"
    @close="closeModal"
  >
    <div class="space-y-4">
      <div>
        <label for="platform" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Platform *</label>
        <select
          id="platform"
          v-model="formData.platform"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        >
          <option v-for="opt in LINK_TYPES" :key="opt.value" :value="opt.value">{{ opt.label }}</option>
        </select>
      </div>

      <div>
        <label for="label" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Label</label>
        <input
          id="label"
          v-model="formData.label"
          type="text"
          placeholder="e.g. Personal Portfolio"
          maxlength="200"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 transition-colors"
          :class="[
            labelValidationError 
              ? 'border-red-500 dark:border-red-500' 
              : 'border-gray-300 dark:border-gray-600'
          ]"
        />
        <div class="flex justify-between mt-1">
          <p v-if="labelValidationError" class="text-red-500 dark:text-red-400 text-sm">
            {{ labelValidationError }}
          </p>
          <p class="text-gray-500 dark:text-gray-400 text-xs ml-auto">
            {{ formData.label.length }}/200
          </p>
        </div>
      </div>

      <div>
        <label for="url" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">URL *</label>
        <input
          id="url"
          v-model="formData.url"
          type="text"
          placeholder="https://example.com"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 transition-colors"
          :class="[
            urlValidationError 
              ? 'border-red-500 dark:border-red-500' 
              : 'border-gray-300 dark:border-gray-600'
          ]"
          required
        />
        <p v-if="urlValidationError" class="text-red-500 dark:text-red-400 text-sm mt-1">
          {{ urlValidationError }}
        </p>
      </div>

      <div class="flex items-center">
        <input v-model="formData.is_visible" type="checkbox" id="is_visible" class="rounded text-purple-600 mr-2" />
        <label for="is_visible" class="text-sm text-gray-700 dark:text-gray-300">Visible on profile</label>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeModal"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors"
        >
          Cancel
        </button>
        <button
          @click="handleSave"
          :disabled="!isFormValid"
          class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Link"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Link?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ linkToDelete?.label }}</span>? This action cannot be undone.
          </p>
        </div>
      </div>
    </div>

    <template #footer>
      <div class="flex justify-end space-x-3">
        <button
          @click="closeDeleteModal"
          :disabled="isDeleting"
          class="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Cancel
        </button>
        <button
          @click="confirmDelete"
          :disabled="isDeleting"
          class="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isDeleting ? 'Deleting...' : 'Delete' }}
        </button>
      </div>
    </template>
  </Modal>
</template>