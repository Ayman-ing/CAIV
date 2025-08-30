<script setup lang="ts">
// filepath: frontend/app/components/profile/project/ProjectSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Project, ProjectFormData, ProjectDisplay } from './types'

// Projects Data
const projects = ref<Project[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingProject = ref<Project | null>(null)

// Form state
const formData = ref<ProjectFormData>({
  title: '',
  description: '',
  startDate: '',
  endDate: '',
  projectUrl: '',
  isOngoing: false
})

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingProject.value = null
  formData.value = {
    title: '',
    description: '',
    startDate: '',
    endDate: '',
    projectUrl: '',
    isOngoing: false
  }
  isModalOpen.value = true
}

const openEditModal = (project: Project) => {
  isEditing.value = true
  editingProject.value = project
  formData.value = {
    title: project.title,
    description: project.description || '',
    startDate: project.startDate,
    endDate: project.endDate || '',
    projectUrl: project.projectUrl || '',
    isOngoing: !project.endDate
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingProject.value) {
    // Update existing project
    const index = projects.value.findIndex(proj => proj.id === editingProject.value!.id)
    if (index !== -1 && projects.value[index]) {
      projects.value[index] = {
        ...projects.value[index],
        title: formData.value.title.trim(),
        description: formData.value.description.trim() || undefined,
        startDate: formData.value.startDate,
        endDate: formData.value.isOngoing ? undefined : formData.value.endDate,
        projectUrl: formData.value.projectUrl.trim() || undefined
      }
    }
  } else {
    // Add new project
    const newProject: Project = {
      id: Date.now(),
      title: formData.value.title.trim(),
      description: formData.value.description.trim() || undefined,
      startDate: formData.value.startDate,
      endDate: formData.value.isOngoing ? undefined : formData.value.endDate,
      projectUrl: formData.value.projectUrl.trim() || undefined,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    projects.value.push(newProject)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingProject.value = null
  formData.value = {
    title: '',
    description: '',
    startDate: '',
    endDate: '',
    projectUrl: '',
    isOngoing: false
  }
}

const removeProject = (id: number) => {
  const index = projects.value.findIndex(proj => proj.id === id)
  if (index !== -1) {
    projects.value.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return formData.value.title.trim() !== '' && 
         formData.value.startDate !== '' &&
         (formData.value.isOngoing || formData.value.endDate !== '')
})

const hasProjects = computed(() => {
  return projects.value.length > 0
})

const isValidUrl = (url: string): boolean => {
  try {
    new URL(url)
    return true
  } catch {
    return false
  }
}

// Enhanced display data
const displayProjects = computed((): ProjectDisplay[] => {
  return projects.value.map(project => {
    const startDate = new Date(project.startDate)
    const endDate = project.endDate ? new Date(project.endDate) : new Date()
    const monthsDiff = (endDate.getFullYear() - startDate.getFullYear()) * 12 + (endDate.getMonth() - startDate.getMonth())
    
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    const getDurationText = (months: number) => {
      const years = Math.floor(months / 12)
      const remainingMonths = months % 12
      
      if (years === 0) return `${remainingMonths} month${remainingMonths !== 1 ? 's' : ''}`
      if (remainingMonths === 0) return `${years} year${years !== 1 ? 's' : ''}`
      return `${years} year${years !== 1 ? 's' : ''}, ${remainingMonths} month${remainingMonths !== 1 ? 's' : ''}`
    }
    
    return {
      ...project,
      displayDateRange: `${formatDate(project.startDate)} - ${project.endDate ? formatDate(project.endDate) : 'Ongoing'}`,
      durationMonths: monthsDiff,
      durationText: getDurationText(monthsDiff),
      isOngoing: !project.endDate,
      technologies: [],
      features: [],
      hasValidUrl: project.projectUrl ? isValidUrl(project.projectUrl) : false
    } as ProjectDisplay
  }).sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime())
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
    :is-empty="!hasProjects"
    empty-message="Add your projects"
    add-button-text="Add Project"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasProjects" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-orange-50 dark:bg-orange-900/20 rounded-lg border border-orange-200 dark:border-orange-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:folder-multiple" class="w-5 h-5 text-orange-600 dark:text-orange-400" />
            <div>
              <p class="text-sm font-medium text-orange-700 dark:text-orange-300">Total Projects</p>
              <p class="text-xs text-orange-600 dark:text-orange-400">{{ projects.length }} project{{ projects.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-orange-600 hover:bg-orange-700 dark:bg-orange-500 dark:hover:bg-orange-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Project
        </button>
      </div>

      <!-- Projects Grid -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div v-for="project in displayProjects" :key="project.id" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <!-- Ongoing Badge -->
          <div v-if="project.isOngoing" class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800 rounded-full">
              In Progress
            </span>
          </div>
          
          <!-- Project Title -->
          <div class="mb-4">
            <div class="flex items-start justify-between">
              <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-2 pr-4">
                {{ project.title }}
              </h3>
              <div v-if="project.hasValidUrl" class="flex-shrink-0">
                <a
                  :href="project.projectUrl"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="p-1.5 text-gray-400 hover:text-orange-600 dark:hover:text-orange-400 transition-colors"
                  title="View project"
                >
                  <Icon name="mdi:external-link" class="w-4 h-4" />
                </a>
              </div>
            </div>
          </div>
          
          <!-- Date Range & Duration -->
          <div class="flex items-center justify-between mb-4 text-sm text-gray-500 dark:text-gray-400">
            <div class="flex items-center space-x-2">
              <Icon name="mdi:calendar" class="w-4 h-4" />
              <span>{{ project.displayDateRange }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <Icon name="mdi:clock-outline" class="w-4 h-4" />
              <span>{{ project.durationText }}</span>
            </div>
          </div>
          
          <!-- Description -->
          <div v-if="project.description" class="mb-4">
            <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed line-clamp-3">{{ project.description }}</p>
          </div>
          
          <!-- Project URL -->
          <div v-if="project.hasValidUrl" class="mb-4">
            <div class="flex items-center space-x-2 p-2 bg-gray-50 dark:bg-gray-700 rounded border border-gray-200 dark:border-gray-600">
              <Icon name="mdi:link" class="w-4 h-4 text-gray-400" />
              <a
                :href="project.projectUrl"
                target="_blank"
                rel="noopener noreferrer"
                class="text-sm text-orange-600 dark:text-orange-400 hover:underline truncate"
              >
                {{ project.projectUrl }}
              </a>
            </div>
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
              @click="removeProject(project.id!)"
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
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Project' : 'Add Project' }}
      </h2>
    </template>
    
    <div class="space-y-6">
      <!-- Project Title -->
      <div>
        <label for="title" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Project Title *
        </label>
        <input
          id="title"
          v-model="formData.title"
          type="text"
          placeholder="e.g. E-commerce Website, Mobile App, Data Analysis Tool"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Give your project a clear, descriptive name
        </p>
      </div>

      <!-- Date Range -->
      <div class="grid grid-cols-2 gap-4">
        <!-- Start Date -->
        <div>
          <label for="startDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Start Date *
          </label>
          <input
            id="startDate"
            v-model="formData.startDate"
            type="date"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            required
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            When did you start this project?
          </p>
        </div>

        <!-- End Date / Ongoing -->
        <div>
          <label for="endDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            End Date
          </label>
          <input
            id="endDate"
            v-model="formData.endDate"
            type="date"
            :disabled="formData.isOngoing"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
            :required="!formData.isOngoing"
          />
          <div class="mt-2">
            <label class="flex items-center">
              <input
                v-model="formData.isOngoing"
                type="checkbox"
                class="rounded border-gray-300 dark:border-gray-600 text-orange-600 focus:ring-orange-500 dark:bg-gray-700"
              />
              <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">This project is ongoing</span>
            </label>
          </div>
        </div>
      </div>

      <!-- Project URL -->
      <div>
        <label for="projectUrl" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Project URL (Optional)
        </label>
        <input
          id="projectUrl"
          v-model="formData.projectUrl"
          type="url"
          placeholder="https://github.com/user/project or https://myproject.com"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Link to GitHub repository, live demo, or project documentation
        </p>
      </div>

      <!-- Description -->
      <div>
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Project Description
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="6"
          placeholder="Describe your project:&#10;&#10;• What problem does it solve?&#10;• What technologies did you use?&#10;• What was your role?&#10;• What were the key features or achievements?"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Explain the project's purpose, your role, technologies used, and key achievements
        </p>
      </div>

      <!-- Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Project Tips</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li>Focus on projects that demonstrate relevant skills</li>
              <li>Quantify impact where possible (users, performance gains, etc.)</li>
              <li>Include both personal and professional projects</li>
              <li>Mention specific technologies and methodologies used</li>
              <li>Always include a working link if the project is accessible</li>
            </ul>
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
        class="px-4 py-2 bg-orange-600 hover:bg-orange-700 dark:bg-orange-500 dark:hover:bg-orange-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Project' : 'Save Project' }}
      </button>
    </template>
  </Modal>
</template>
