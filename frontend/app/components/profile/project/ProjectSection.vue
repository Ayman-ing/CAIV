<script setup lang="ts">
// filepath: frontend/app/components/profile/project/ProjectSection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useToast } from '~/composables/useToast'
import { useUrlValidator } from '~/composables/useUrlValidator'
import { useFormValidation } from '~/composables/useFormValidation'
import type { Project, ProjectFormData, ProjectDisplay } from './types'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()
const { isValidUrl, getUrlErrorMessage, normalizeUrl } = useUrlValidator()
const { validateLength, validateEndDate } = useFormValidation()

// Validation errors
const urlValidationError = ref<string | null>(null)
const nameValidationError = ref<string | null>(null)
const descriptionValidationError = ref<string | null>(null)
const technologiesValidationError = ref<string | null>(null)
const endDateValidationError = ref<string | null>(null)

// Projects Data
const projects = ref<Project[]>([])
const isExpanded = ref(false)
const isLoading = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingProject = ref<Project | null>(null)

// Delete confirmation modal state
const isDeleteModalOpen = ref(false)
const projectToDelete = ref<Project | null>(null)
const isDeleting = ref(false)

// Form state
const formData = ref<ProjectFormData>({
  name: '',
  description: '',
  technologies: '',
  start_date: '',
  end_date: '',
  url: '',
  isOngoing: false
})

onMounted(async () => {
  await fetchProjects()
})

const fetchProjects = async () => {
  if (!activeProfile.value?.uuid) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.getAllProjects(activeProfile.value.uuid)
    projects.value = data
  } catch (error) {
    console.error('Failed to fetch projects:', error)
  } finally {
    isLoading.value = false
  }
}

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingProject.value = null
  formData.value = {
    name: '',
    description: '',
    technologies: '',
    start_date: '',
    end_date: '',
    url: '',
    isOngoing: false
  }
  isModalOpen.value = true
}

const openEditModal = (proj: Project) => {
  isEditing.value = true
  editingProject.value = proj
  formData.value = {
    name: proj.name,
    description: proj.description || '',
    technologies: proj.technologies || '',
    start_date: proj.start_date,
    end_date: proj.end_date || '',
    url: proj.url || '',
    isOngoing: !proj.end_date
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value?.uuid) return
  
  // Validate name
  const nameError = validateLength(formData.value.name, 1, 200)
  if (nameError) {
    nameValidationError.value = nameError
    return
  }
  nameValidationError.value = null
  
  // Validate description
  const descError = validateLength(formData.value.description, undefined, 2000)
  if (descError) {
    descriptionValidationError.value = descError
    return
  }
  descriptionValidationError.value = null
  
  // Validate technologies
  const techError = validateLength(formData.value.technologies, undefined, 1000)
  if (techError) {
    technologiesValidationError.value = techError
    return
  }
  technologiesValidationError.value = null
  
  // Validate end date
  if (!formData.value.isOngoing && formData.value.end_date) {
    const endDateError = validateEndDate(formData.value.end_date, formData.value.start_date)
    if (endDateError) {
      endDateValidationError.value = endDateError
      return
    }
  }
  endDateValidationError.value = null
  
  // Validate URL if provided
  if (formData.value.url.trim()) {
    const urlError = getUrlErrorMessage(formData.value.url)
    if (urlError) {
      urlValidationError.value = urlError
      return
    }
  }
  urlValidationError.value = null
  
  const payload: Omit<Project, 'uuid'> = {
    name: formData.value.name.trim(),
    description: formData.value.description.trim() || null,
    technologies: formData.value.technologies.trim() || null,
    start_date: formData.value.start_date,
    end_date: formData.value.isOngoing ? null : formData.value.end_date,
    url: formData.value.url.trim() ? normalizeUrl(formData.value.url) : null
  }

  try {
    if (isEditing.value && editingProject.value) {
      await profileSectionsService.updateProject(
        activeProfile.value.uuid,
        editingProject.value.uuid,
        payload
      )
      success('Project updated successfully!')
    } else {
      await profileSectionsService.createProject(activeProfile.value.uuid, payload)
      success('Project added successfully!')
    }
    await fetchProjects()
    closeModal()
  } catch (err) {
    console.error('Failed to save project:', err)
    error(`Failed to save project: ${err instanceof Error ? err.message : 'Unknown error'}`)
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingProject.value = null
}

const openDeleteModal = (project: Project) => {
  projectToDelete.value = project
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  projectToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value?.uuid || !projectToDelete.value) return
  
  isDeleting.value = true
  try {
    await profileSectionsService.deleteProject(activeProfile.value.uuid, projectToDelete.value.uuid)
    await fetchProjects()
    closeDeleteModal()
    success('Project deleted successfully!')
  } catch (err) {
    console.error('Failed to delete project:', err)
    error(`Failed to delete project: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const isFormValid = computed(() => {
  return formData.value.name.trim() !== '' && 
         formData.value.start_date !== '' &&
         (formData.value.isOngoing || formData.value.end_date !== '')
})

const hasProjects = computed(() => {
  return projects.value.length > 0
})

// Enhanced display data
const displayProjects = computed((): ProjectDisplay[] => {
  return projects.value.map(project => {
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    return {
      ...project,
      displayDateRange: `${formatDate(project.start_date)} - ${project.end_date ? formatDate(project.end_date) : 'Ongoing'}`,
      durationText: '', 
      isOngoing: !project.end_date,
      hasValidUrl: project.url ? isValidUrl(project.url) : false
    } as ProjectDisplay
  }).sort((a, b) => new Date(b.start_date).getTime() - new Date(a.start_date).getTime())
})
</script>

<template>
  <CollapsibleSection
    title="Projects"
    description="Showcase your notable projects and work"
    icon="mdi:rocket-launch"
    icon-color="text-orange-600 dark:text-orange-400"
    icon-bg-color="bg-orange-100 dark:bg-orange-900/30"
    button-color="bg-orange-600 dark:bg-orange-500 hover:bg-orange-700 dark:hover:bg-orange-600"
    :is-expanded="isExpanded"
    :is-empty="!isLoading && projects.length === 0"
    empty-message="Add your projects"
    add-button-text="Add Project"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-orange-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="hasProjects" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-yellow-50 dark:bg-yellow-900/20 rounded-lg border border-yellow-200 dark:border-yellow-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:briefcase" class="w-5 h-5 text-yellow-600 dark:text-yellow-400" />
            <div>
              <p class="text-sm font-medium text-yellow-700 dark:text-yellow-300">Projects</p>
              <p class="text-xs text-yellow-600 dark:text-yellow-400">{{ displayProjects.length }} project{{ displayProjects.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-yellow-600 hover:bg-yellow-700 dark:bg-yellow-500 dark:hover:bg-yellow-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Project
        </button>
      </div>

      <!-- Projects List -->
      <div class="space-y-6">
        <div v-for="project in displayProjects" :key="project.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
        <!-- Ongoing Badge -->
        <div v-if="project.isOngoing" class="absolute top-4 right-4">
          <span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800 rounded-full">
            In Progress
          </span>
        </div>
        
        <!-- Project Title -->
        <div class="mb-4">
          <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2">
            {{ project.name }}
          </h3>
          <div v-if="project.url && project.hasValidUrl" class="text-sm text-orange-600 dark:text-orange-400 hover:underline">
            <a :href="project.url" target="_blank" rel="noopener noreferrer" class="flex items-center">
              <Icon name="mdi:link" class="w-4 h-4 mr-1" />
              {{ project.url }}
            </a>
          </div>
        </div>
        
        <!-- Date Range -->
        <div class="flex items-center space-x-2 text-sm text-gray-500 dark:text-gray-400 mb-4">
          <Icon name="mdi:calendar" class="w-4 h-4" />
          <span>{{ project.displayDateRange }}</span>
        </div>
        
        <!-- Technologies -->
        <div v-if="project.technologies" class="mb-4">
          <div class="flex flex-wrap gap-2">
            <span v-for="tech in project.technologies.split(',')" :key="tech" class="px-2 py-1 text-xs bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded">
              {{ tech.trim() }}
            </span>
          </div>
        </div>

        <!-- Description -->
        <div v-if="project.description" class="mb-4">
          <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed line-clamp-3">{{ project.description }}</p>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
          <button
            @click="openEditModal(project)"
            class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
          >
            <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
            Edit
          </button>
          
          <button
            @click="openDeleteModal(project)"
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
    :title="isEditing ? 'Edit Project' : 'Add Project'"
    size="xl"
    @close="closeModal"
  >
    <div class="space-y-6">
      <div>
        <label for="name" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Project Name *
        </label>
        <input
          id="name"
          v-model="formData.name"
          type="text"
          placeholder="e.g. Portfolio Website"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
      </div>

      <div class="grid grid-cols-2 gap-4">
        <div>
          <label for="start_date" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Start Date *
          </label>
          <input
            id="start_date"
            v-model="formData.start_date"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
            :disabled="formData.isOngoing"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50"
          />
          <div class="mt-2">
            <label class="flex items-center text-sm">
              <input v-model="formData.isOngoing" type="checkbox" class="rounded text-orange-600 mr-2" />
              This project is ongoing
            </label>
          </div>
        </div>
      </div>

      <div>
        <label for="url" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Project URL
        </label>
        <input
          id="url"
          v-model="formData.url"
          type="text"
          placeholder="https://github.com/... (optional)"
          class="w-full px-3 py-2 border rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 transition-colors"
          :class="[
            urlValidationError 
              ? 'border-red-500 dark:border-red-500' 
              : 'border-gray-300 dark:border-gray-600'
          ]"
        />
        <p v-if="urlValidationError" class="text-red-500 dark:text-red-400 text-sm mt-1">
          {{ urlValidationError }}
        </p>
      </div>

      <div>
        <label for="technologies" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Technologies (Comma separated)
        </label>
        <input
          id="technologies"
          v-model="formData.technologies"
          type="text"
          placeholder="Vue.js, FastAPI, PostgreSQL"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
      </div>

      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="4"
          placeholder="What did you build? What was your impact?"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
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
          class="px-4 py-2 bg-orange-600 hover:bg-orange-700 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {{ isEditing ? 'Update' : 'Save' }}
        </button>
      </div>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Project"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400 flex-shrink-0" />
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Project?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ projectToDelete?.name }}</span>? This action cannot be undone.
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
