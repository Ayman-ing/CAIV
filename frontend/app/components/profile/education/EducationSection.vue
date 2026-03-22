<script setup lang="ts">
// filepath: frontend/app/components/profile/education/EducationSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useToast } from '~/composables/useToast'
import type { Education, EducationFormData, EducationDisplay } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

// Education Data
const educationList = ref<Education[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingEducation = ref<Education | null>(null)

// Delete confirmation modal state
const isDeleteModalOpen = ref(false)
const educationToDelete = ref<Education | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<EducationFormData>({
  institution: '',
  degree: '',
  degree_type: 'Other',
  field_of_study: '',
  honors: '',
  gpa: '',
  start_date: '',
  end_date: '',
  description: '',
  isOngoing: false
})

// Predefined options
const degreeTypes = [
  'High School Diploma', 'Associate', 'Bachelor', 'Master', 'PhD',
  'Professional', 'Certificate', 'Other'
]

onMounted(async () => {
  await fetchEducation()
})

const fetchEducation = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllEducations(activeProfile.value.uuid)
    educationList.value = data
  } catch (error) {
    console.error('Failed to fetch education:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingEducation.value = null
  formData.value = {
    institution: '',
    degree: '',
    degree_type: 'Bachelor',
    field_of_study: '',
    honors: '',
    gpa: '',
    start_date: '',
    end_date: '',
    description: '',
    isOngoing: false
  }
  isModalOpen.value = true
}

const openEditModal = (education: Education) => {
  isEditing.value = true
  editingEducation.value = education
  formData.value = {
    institution: education.institution,
    degree: education.degree,
    degree_type: education.degree_type || 'Other',
    field_of_study: education.field_of_study || '',
    honors: education.honors || '',
    gpa: education.gpa?.toString() || '',
    start_date: education.start_date,
    end_date: education.end_date || '',
    description: education.description || '',
    isOngoing: !education.end_date
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  const payload: Omit<Education, 'uuid'> = {
    institution: formData.value.institution.trim(),
    degree: formData.value.degree.trim(),
    degree_type: formData.value.degree_type,
    field_of_study: formData.value.field_of_study.trim() || null,
    honors: formData.value.honors.trim() || null,
    gpa: formData.value.gpa ? parseFloat(formData.value.gpa) : null,
    start_date: formData.value.start_date,
    end_date: formData.value.isOngoing ? null : formData.value.end_date,
    description: formData.value.description.trim() || null
  }

  try {
    if (isEditing.value && editingEducation.value) {
      await profileSectionsService.updateEducation(
        activeProfile.value.uuid,
        editingEducation.value.uuid,
        payload
      )
      success('Education updated successfully!')
    } else {
      await profileSectionsService.createEducation(activeProfile.value.uuid, payload)
      success('Education added successfully!')
    }
    await fetchEducation()
    closeModal()
  } catch (err) {
    console.error('Failed to save education:', err)
    error(`Failed to save education: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingEducation.value = null
}

const openDeleteModal = (education: Education) => {
  educationToDelete.value = education
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  educationToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !educationToDelete.value) return
  
  isDeleting.value = true
  try {
    await profileSectionsService.deleteEducation(activeProfile.value.uuid, educationToDelete.value.uuid)
    await fetchEducation()
    closeDeleteModal()
    success('Education deleted successfully!')
  } catch (err) {
    console.error('Failed to delete education:', err)
    error(`Failed to delete education: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.institution.trim() !== '' && 
         formData.value.degree.trim() !== '' && 
         formData.value.start_date !== '' &&
         (formData.value.isOngoing || formData.value.end_date !== '')
})

const hasEducation = computed(() => {
  return educationList.value.length > 0
})

// Enhanced display data
const displayEducation = computed((): EducationDisplay[] => {
  return educationList.value.map(edu => {
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    return {
      ...edu,
      displayDateRange: `${formatDate(edu.start_date)} - ${edu.end_date ? formatDate(edu.end_date) : 'Present'}`,
      isCompleted: !!edu.end_date,
      completionYear: edu.end_date ? new Date(edu.end_date).getFullYear() : undefined
    } as EducationDisplay
  }).sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime())
})
</script>

<template>
  <CollapsibleSection
    title="Education"
    description="Your educational background and qualifications"
    icon="mdi:school"
    icon-color="text-green-600 dark:text-green-400"
    icon-bg-color="bg-green-100 dark:bg-green-900/30"
    button-color="bg-green-600 dark:bg-green-500 hover:bg-green-700 dark:hover:bg-green-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && !hasEducation"
    empty-message="Add your education"
    add-button-text="Add Education"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-green-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasEducation" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:school-outline" class="w-5 h-5 text-green-600 dark:text-green-400" />
            <div>
              <p class="text-sm font-medium text-green-700 dark:text-green-300">Education Records</p>
              <p class="text-xs text-green-600 dark:text-green-400">{{ educationList.length }} record{{ educationList.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Education
        </button>
      </div>

      <!-- Education Timeline -->
      <div class="space-y-4">
        <div v-for="education in displayEducation" :key="education.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <!-- Ongoing Badge -->
          <div v-if="!education.isCompleted" class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-full">
              In Progress
            </span>
          </div>
          
          <!-- Degree & Field -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
              {{ education.degree }}{{ education.field_of_study ? ` in ${education.field_of_study}` : '' }}
            </h3>
            <div class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <Icon name="mdi:school" class="w-4 h-4" />
              <span class="font-medium">{{ education.institution }}</span>
            </div>
          </div>
          
          <!-- Date Range & GPA -->
          <div class="flex items-center justify-between mb-4 text-sm text-gray-500 dark:text-gray-400">
            <div class="flex items-center space-x-2">
              <Icon name="mdi:calendar" class="w-4 h-4" />
              <span>{{ education.displayDateRange }}</span>
            </div>
            <div v-if="education.gpa" class="flex items-center space-x-2">
              <Icon name="mdi:chart-line" class="w-4 h-4" />
              <span>GPA: {{ education.gpa }}</span>
            </div>
          </div>
          
          <!-- Honors -->
          <div v-if="education.honors" class="mb-4">
            <div class="flex items-center space-x-2 text-amber-600 dark:text-amber-400">
              <Icon name="mdi:medal" class="w-4 h-4" />
              <span class="font-medium">{{ education.honors }}</span>
            </div>
          </div>
          
          <!-- Description -->
          <div v-if="education.description" class="mb-4">
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed text-sm">{{ education.description }}</p>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              @click="openEditModal(education)"
              class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
            >
              <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
              Edit
            </button>
            
            <button
              @click="openDeleteModal(education)"
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
    :title="isEditing ? 'Edit Education' : 'Add Education'"
    size="xl"
    @close="closeModal"
  >
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Education' : 'Add Education' }}
      </h2>
    </template>
    
    <div class="grid grid-cols-2 gap-6">
      <!-- Institution -->
      <div class="col-span-2">
        <label for="institution" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Institution *
        </label>
        <input
          id="institution"
          v-model="formData.institution"
          type="text"
          placeholder="e.g. University of Technology"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <!-- Degree Type -->
      <div>
        <label for="degree_type" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Degree Type *
        </label>
        <select
          id="degree_type"
          v-model="formData.degree_type"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option v-for="type in degreeTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>

      <!-- Degree Name -->
      <div>
        <label for="degree" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Degree Name *
        </label>
        <input
          id="degree"
          v-model="formData.degree"
          type="text"
          placeholder="e.g. Bachelor of Science"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <!-- Field of Study -->
      <div>
        <label for="field_of_study" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Field of Study
        </label>
        <input
          id="field_of_study"
          v-model="formData.field_of_study"
          type="text"
          placeholder="e.g. Computer Science"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
      </div>

      <!-- GPA -->
      <div>
        <label for="gpa" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          GPA / Moyenne (0 - 20)
        </label>
        <input
          id="gpa"
          v-model="formData.gpa"
          type="number"
          step="0.01"
          min="0"
          max="20"
          placeholder="e.g. 16.5 (Tunisia) or 3.75 (US/4.0 scale)"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
      </div>

      <!-- Start Date -->
      <div>
        <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Start Date *
        </label>
        <input
          id="start_date"
          v-model="formData.start_date"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <!-- End Date -->
      <div>
        <label for="end_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          End Date
        </label>
        <input
          id="end_date"
          v-model="formData.end_date"
          type="date"
          :disabled="formData.isOngoing"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50"
        />
        <div class="mt-2">
          <label class="flex items-center text-sm">
            <input v-model="formData.isOngoing" type="checkbox" class="rounded text-green-600 mr-2" />
            Currently enrolled
          </label>
        </div>
      </div>

      <!-- Honors -->
      <div class="col-span-2">
        <label for="honors" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Honors & Awards
        </label>
        <input
          id="honors"
          v-model="formData.honors"
          type="text"
          placeholder="e.g. Dean's List, Cum Laude"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
      </div>

      <!-- Description -->
      <div class="col-span-2">
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="3"
          placeholder="Relevant coursework, projects, etc."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
          class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Education"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <div class="flex-shrink-0">
          <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400" />
        </div>
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Education?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ educationToDelete?.degree }}</span> from <span class="font-semibold">{{ educationToDelete?.institution }}</span>? This action cannot be undone.
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
