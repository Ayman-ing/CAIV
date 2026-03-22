<script setup lang="ts">
// filepath: frontend/app/components/profile/custom/CustomSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useToast } from '~/composables/useToast'
import type { CustomSection, CustomSectionFormData } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'

const profileStore = useProfileStore()
const activeProfileUuid = computed(() => profileStore.activeProfile.value?.uuid)
const { success, error } = useToast()

// Custom Sections Data
const customSections = ref<CustomSection[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingSection = ref<CustomSection | null>(null)

// Delete confirmation modal state
const isDeleteModalOpen = ref(false)
const sectionToDelete = ref<CustomSection | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<CustomSectionFormData>({
  title: '',
  content: ''
})

onMounted(async () => {
  await fetchSections()
})

const fetchSections = async () => {
  if (!activeProfileUuid.value) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllCustomSections(activeProfileUuid.value)
    customSections.value = data
  } catch (error) {
    console.error('Failed to fetch custom sections:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingSection.value = null
  formData.value = {
    title: '',
    content: ''
  }
  isModalOpen.value = true
}

const openEditModal = (section: CustomSection) => {
  isEditing.value = true
  editingSection.value = section
  formData.value = {
    title: section.title,
    content: section.content
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfileUuid.value) return
  
  const payload: Omit<CustomSection, 'uuid'> = {
    title: formData.value.title.trim(),
    content: formData.value.content.trim()
  }

  try {
    if (isEditing.value && editingSection.value) {
      await profileSectionsService.updateCustomSection(
        activeProfileUuid.value,
        editingSection.value.uuid,
        payload
      )
      success('Custom section updated successfully!')
    } else {
      await profileSectionsService.createCustomSection(activeProfileUuid.value, payload)
      success('Custom section added successfully!')
    }
    await fetchSections()
    closeModal()
  } catch (err) {
    console.error('Failed to save custom section:', err)
    error(`Failed to save custom section: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingSection.value = null
}

const openDeleteModal = (section: CustomSection) => {
  sectionToDelete.value = section
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  sectionToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfileUuid.value || !sectionToDelete.value) return
  
  isDeleting.value = true
  try {
    await profileSectionsService.deleteCustomSection(activeProfileUuid.value, sectionToDelete.value.uuid)
    await fetchSections()
    closeDeleteModal()
    success('Custom section deleted successfully!')
  } catch (err) {
    console.error('Failed to delete custom section:', err)
    error(`Failed to delete custom section: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const removeSection = async (uuid: string) => {
  if (!activeProfileUuid.value) return
  if (!confirm('Are you sure you want to delete this section?')) return
  
  try {
    await profileSectionsService.deleteCustomSection(activeProfileUuid.value, uuid)
    await fetchSections()
  } catch (error) {
    console.error('Failed to delete custom section:', error)
  }
}

const isFormValid = computed(() => {
  return formData.value.title.trim() !== '' && formData.value.content.trim() !== ''
})

const hasSections = computed(() => customSections.value.length > 0)
</script>

<template>
  <CollapsibleSection
    title="Custom Sections"
    description="Add unique sections like Awards, Volunteering, or Publications"
    icon="mdi:playlist-plus"
    icon-color="text-pink-600 dark:text-pink-400"
    icon-bg-color="bg-pink-100 dark:bg-pink-900/30"
    button-color="bg-pink-600 dark:bg-pink-500 hover:bg-pink-700 dark:hover:bg-pink-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && customSections.length === 0"
    empty-message="Add custom sections"
    add-button-text="Add Section"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-pink-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasSections" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-pink-50 dark:bg-pink-900/20 rounded-lg border border-pink-200 dark:border-pink-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:note-text" class="w-5 h-5 text-pink-600 dark:text-pink-400" />
            <div>
              <p class="text-sm font-medium text-pink-700 dark:text-pink-300">Custom Sections</p>
              <p class="text-xs text-pink-600 dark:text-pink-400">{{ customSections.length }} section{{ customSections.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-pink-600 hover:bg-pink-700 dark:bg-pink-500 dark:hover:bg-pink-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Section
        </button>
      </div>

      <!-- Custom Sections List -->
      <div class="space-y-6">
        <div v-for="section in customSections" :key="section.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start justify-between mb-4">
          <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100">{{ section.title }}</h3>
          <div class="flex items-center space-x-2">
            <button @click="openEditModal(section)" class="p-2 text-gray-400 hover:text-pink-600 transition-colors">
              <Icon name="mdi:pencil" class="w-5 h-5" />
            </button>
            <button @click="openDeleteModal(section)" class="p-2 text-gray-400 hover:text-red-600 transition-colors">
              <Icon name="mdi:delete" class="w-5 h-5" />
            </button>
          </div>
        </div>
        <div class="prose dark:prose-invert max-w-none text-gray-700 dark:text-gray-300 whitespace-pre-wrap">
          {{ section.content }}
        </div>
      </div>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Custom Section' : 'Add Custom Section'"
    size="xl"
    @close="closeModal"
  >
    <div class="space-y-6">
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Section Title *
        </label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          placeholder="e.g. Awards & Recognitions"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div>
        <label for="content" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Content *
        </label>
        <textarea
          id="content"
          v-model="formData.content"
          rows="10"
          placeholder="Describe your achievements, volunteering work, or any other information..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-pink-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        ></textarea>
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
          class="px-4 py-2 bg-pink-600 hover:bg-pink-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Custom Section"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <div class="flex-shrink-0">
          <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400" />
        </div>
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Section?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ sectionToDelete?.title }}</span>? This action cannot be undone.
          </p>
        </div>
      </div>
    </div>

    <template #footer>
      <button
        @click="closeDeleteModal"
        :disabled="isDeleting"
        class="px-4 py-2 bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-200 rounded-lg hover:bg-gray-400 dark:hover:bg-gray-500 transition-colors disabled:opacity-50"
      >
        Cancel
      </button>
      
      <button
        @click="confirmDelete"
        :disabled="isDeleting"
        class="px-4 py-2 bg-red-600 hover:bg-red-700 dark:bg-red-500 dark:hover:bg-red-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon v-if="!isDeleting" name="mdi:delete" class="w-4 h-4 mr-2" />
        <Icon v-else name="mdi:loading" class="w-4 h-4 mr-2 animate-spin" />
        {{ isDeleting ? 'Deleting...' : 'Delete' }}
      </button>
    </template>
  </Modal>
</template>
