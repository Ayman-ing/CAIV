<script setup lang="ts">
// filepath: frontend/app/components/profile/experience/ExperienceSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useToast } from '~/composables/useToast'
import type { WorkExperience, ExperienceFormData, ExperienceDisplay } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

// Experience Data
const experienceList = ref<WorkExperience[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingExperience = ref<WorkExperience | null>(null)

// Delete confirmation modal state
const isDeleteModalOpen = ref(false)
const experienceToDelete = ref<WorkExperience | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<ExperienceFormData>({
  job_title: '',
  company: '',
  start_date: '',
  end_date: '',
  description: '',
  isCurrentJob: false
})

onMounted(async () => {
  await fetchExperience()
})

const fetchExperience = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllWorkExperiences(activeProfile.value.uuid)
    experienceList.value = data
  } catch (error) {
    console.error('Failed to fetch work experience:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingExperience.value = null
  formData.value = {
    job_title: '',
    company: '',
    start_date: '',
    end_date: '',
    description: '',
    isCurrentJob: false
  }
  isModalOpen.value = true
}

const openEditModal = (exp: WorkExperience) => {
  isEditing.value = true
  editingExperience.value = exp
  formData.value = {
    job_title: exp.job_title,
    company: exp.company,
    start_date: exp.start_date,
    end_date: exp.end_date || '',
    description: exp.description || '',
    isCurrentJob: !exp.end_date
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  const payload: Omit<WorkExperience, 'uuid'> = {
    job_title: formData.value.job_title.trim(),
    company: formData.value.company.trim(),
    description: formData.value.description.trim() || null,
    start_date: formData.value.start_date,
    end_date: formData.value.isCurrentJob ? null : formData.value.end_date
  }

  try {
    if (isEditing.value && editingExperience.value) {
      await profileSectionsService.updateWorkExperience(
        activeProfile.value.uuid,
        editingExperience.value.uuid,
        payload
      )
      success('Work experience updated successfully!')
    } else {
      await profileSectionsService.createWorkExperience(activeProfile.value.uuid, payload)
      success('Work experience added successfully!')
    }
    await fetchExperience()
    closeModal()
  } catch (err) {
    console.error('Failed to save work experience:', err)
    error(`Failed to save work experience: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingExperience.value = null
}

const openDeleteModal = (experience: WorkExperience) => {
  experienceToDelete.value = experience
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  experienceToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !experienceToDelete.value) return
  
  isDeleting.value = true
  try {
    await profileSectionsService.deleteWorkExperience(activeProfile.value.uuid, experienceToDelete.value.uuid)
    await fetchExperience()
    closeDeleteModal()
    success('Work experience deleted successfully!')
  } catch (err) {
    console.error('Failed to delete work experience:', err)
    error(`Failed to delete work experience: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.job_title.trim() !== '' && 
         formData.value.company.trim() !== '' && 
         formData.value.start_date !== '' &&
         (formData.value.isCurrentJob || formData.value.end_date !== '')
})

const hasExperience = computed(() => {
  return experienceList.value.length > 0
})

// Enhanced display data
const displayExperience = computed((): ExperienceDisplay[] => {
  return experienceList.value.map(exp => {
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    return {
      ...exp,
      displayDateRange: `${formatDate(exp.start_date)} - ${exp.end_date ? formatDate(exp.end_date) : 'Present'}`,
      isCurrentPosition: !exp.end_date,
      durationText: '' // Simplified for now
    } as ExperienceDisplay
  }).sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime())
})
</script>

<template>
  <CollapsibleSection
    title="Work Experience"
    description="Your professional history and career milestones"
    icon="mdi:briefcase"
    icon-color="text-blue-600 dark:text-blue-400"
    icon-bg-color="bg-blue-100 dark:bg-blue-900/30"
    button-color="bg-blue-600 dark:bg-blue-500 hover:bg-blue-700 dark:hover:bg-blue-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && experienceList.length === 0"
    empty-message="Add your work experience"
    add-button-text="Add Experience"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-blue-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasExperience" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:briefcase-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400" />
            <div>
              <p class="text-sm font-medium text-blue-700 dark:text-blue-300">Experience</p>
              <p class="text-xs text-blue-600 dark:text-blue-400">{{ displayExperience.length }} position{{ displayExperience.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Experience
        </button>
      </div>

      <!-- Experience List -->
      <div class="space-y-6">
        <div v-for="exp in displayExperience" :key="exp.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <!-- Current Job Badge -->
        <div v-if="exp.isCurrentPosition" class="absolute top-4 right-4">
          <span class="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-full">
            Current Position
          </span>
        </div>
        
        <!-- Job Title & Company -->
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
            {{ exp.job_title }}
          </h3>
          <div class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
            <Icon name="mdi:office-building" class="w-4 h-4" />
            <span class="font-medium">{{ exp.company }}</span>
          </div>
        </div>
        
        <!-- Date Range -->
        <div class="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400 mb-4">
          <Icon name="mdi:calendar" class="w-4 h-4" />
          <span>{{ exp.displayDateRange }}</span>
        </div>
        
        <!-- Description -->
        <div v-if="exp.description" class="mb-4">
          <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed text-sm">{{ exp.description }}</p>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            @click="openEditModal(exp)"
            class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
          >
            <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
            Edit
          </button>
          
          <button
            @click="openDeleteModal(exp)"
            class="px-3 py-1.5 text-sm bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors flex items-center"
          >
            <Icon name="mdi:delete" class="w-4 h-4 mr-1" />
            Remove
          </button>
        </div>
      </div>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Experience' : 'Add Experience'"
    size="xl"
    @close="closeModal"
  >
    <div class="grid grid-cols-2 gap-6">
      <div class="col-span-2">
        <label for="job_title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Title *
        </label>
        <input
          id="job_title"
          v-model="formData.job_title"
          type="text"
          placeholder="e.g. Senior Software Engineer"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div class="col-span-2">
        <label for="company" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Company *
        </label>
        <input
          id="company"
          v-model="formData.company"
          type="text"
          placeholder="e.g. Apple Inc."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Start Date *
        </label>
        <input
          id="start_date"
          v-model="formData.start_date"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          End Date
        </label>
        <input
          id="end_date"
          v-model="formData.end_date"
          type="date"
          :disabled="formData.isCurrentJob"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50"
        />
        <div class="mt-2">
          <label class="flex items-center text-sm text-gray-600 dark:text-gray-400">
            <input v-model="formData.isCurrentJob" type="checkbox" class="rounded text-blue-600 mr-2" />
            Currently working here
          </label>
        </div>
      </div>

      <div class="col-span-2">
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="4"
          placeholder="What did you do? Achievements, responsibilities..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Work Experience"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Work Experience?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ experienceToDelete?.job_title }}</span> at <span class="font-semibold">{{ experienceToDelete?.company }}</span>? This action cannot be undone.
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
