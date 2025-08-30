<script setup lang="ts">
// filepath: frontend/app/components/profile/experience/ExperienceSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { WorkExperience, ExperienceFormData, ExperienceDisplay } from './types'

// Work Experience Data
const workExperiences = ref<WorkExperience[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingExperience = ref<WorkExperience | null>(null)

// Form state
const formData = ref<ExperienceFormData>({
  jobTitle: '',
  company: '',
  startDate: '',
  endDate: '',
  description: '',
  isCurrentJob: false
})

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingExperience.value = null
  formData.value = {
    jobTitle: '',
    company: '',
    startDate: '',
    endDate: '',
    description: '',
    isCurrentJob: false
  }
  isModalOpen.value = true
}

const openEditModal = (experience: WorkExperience) => {
  isEditing.value = true
  editingExperience.value = experience
  formData.value = {
    jobTitle: experience.jobTitle,
    company: experience.company,
    startDate: experience.startDate,
    endDate: experience.endDate || '',
    description: experience.description || '',
    isCurrentJob: !experience.endDate
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingExperience.value) {
    // Update existing experience
    const index = workExperiences.value.findIndex(exp => exp.id === editingExperience.value!.id)
    if (index !== -1 && workExperiences.value[index]) {
      workExperiences.value[index] = {
        ...workExperiences.value[index],
        jobTitle: formData.value.jobTitle.trim(),
        company: formData.value.company.trim(),
        startDate: formData.value.startDate,
        endDate: formData.value.isCurrentJob ? undefined : formData.value.endDate,
        description: formData.value.description.trim()
      }
    }
  } else {
    // Add new experience
    const newExperience: WorkExperience = {
      id: Date.now(),
      jobTitle: formData.value.jobTitle.trim(),
      company: formData.value.company.trim(),
      startDate: formData.value.startDate,
      endDate: formData.value.isCurrentJob ? undefined : formData.value.endDate,
      description: formData.value.description.trim(),
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    workExperiences.value.push(newExperience)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingExperience.value = null
  formData.value = {
    jobTitle: '',
    company: '',
    startDate: '',
    endDate: '',
    description: '',
    isCurrentJob: false
  }
}

const removeExperience = (id: number) => {
  const index = workExperiences.value.findIndex(exp => exp.id === id)
  if (index !== -1) {
    workExperiences.value.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return formData.value.jobTitle.trim() !== '' && 
         formData.value.company.trim() !== '' && 
         formData.value.startDate !== '' &&
         (formData.value.isCurrentJob || formData.value.endDate !== '')
})

const hasExperience = computed(() => {
  return workExperiences.value.length > 0
})

// Enhanced display data with calculations
const displayExperiences = computed((): ExperienceDisplay[] => {
  return workExperiences.value.map(exp => {
    const startDate = new Date(exp.startDate)
    const endDate = exp.endDate ? new Date(exp.endDate) : new Date()
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
      ...exp,
      displayDateRange: `${formatDate(exp.startDate)} - ${exp.endDate ? formatDate(exp.endDate) : 'Present'}`,
      durationMonths: monthsDiff,
      durationText: getDurationText(monthsDiff),
      isCurrentPosition: !exp.endDate,
      achievements: [] // TODO: Parse description for achievements
    } as ExperienceDisplay
  }).sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime())
})

const totalExperience = computed(() => {
  const totalMonths = displayExperiences.value.reduce((sum, exp) => sum + exp.durationMonths, 0)
  const years = Math.floor(totalMonths / 12)
  const months = totalMonths % 12
  
  if (years === 0) return `${months} month${months !== 1 ? 's' : ''}`
  if (months === 0) return `${years} year${years !== 1 ? 's' : ''}`
  return `${years} year${years !== 1 ? 's' : ''}, ${months} month${months !== 1 ? 's' : ''}`
})
</script>

<template>
  <CollapsibleSection
    title="Work Experience"
    description="Your professional work history"
    icon="mdi:briefcase"
    icon-color="text-indigo-600 dark:text-indigo-400"
    icon-bg-color="bg-indigo-100 dark:bg-indigo-900/30"
    button-color="bg-indigo-600 dark:bg-indigo-500 hover:bg-indigo-700 dark:hover:bg-indigo-600"
    :is-expanded="isExpanded"
    :is-empty="!hasExperience"
    empty-message="Add your work experience"
    add-button-text="Add Experience"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasExperience" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-indigo-50 dark:bg-indigo-900/20 rounded-lg border border-indigo-200 dark:border-indigo-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:briefcase-check" class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <div>
              <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">Total Experience</p>
              <p class="text-xs text-indigo-600 dark:text-indigo-400">{{ totalExperience }}</p>
            </div>
          </div>
          
          <div class="flex items-center space-x-2">
            <Icon name="mdi:office-building" class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
            <div>
              <p class="text-sm font-medium text-indigo-700 dark:text-indigo-300">Positions</p>
              <p class="text-xs text-indigo-600 dark:text-indigo-400">{{ workExperiences.length }} role{{ workExperiences.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Experience
        </button>
      </div>

      <!-- Experience Timeline -->
      <div class="space-y-4">
        <div v-for="experience in displayExperiences" :key="experience.id" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <!-- Current Position Badge -->
          <div v-if="experience.isCurrentPosition" class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800 rounded-full">
              Current Position
            </span>
          </div>
          
          <!-- Job Title & Company -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
              {{ experience.jobTitle }}
            </h3>
            <div class="flex items-center space-x-2 text-gray-600 dark:text-gray-400">
              <Icon name="mdi:office-building" class="w-4 h-4" />
              <span class="font-medium">{{ experience.company }}</span>
            </div>
          </div>
          
          <!-- Date Range & Duration -->
          <div class="flex items-center justify-between mb-4 text-sm text-gray-500 dark:text-gray-400">
            <div class="flex items-center space-x-2">
              <Icon name="mdi:calendar" class="w-4 h-4" />
              <span>{{ experience.displayDateRange }}</span>
            </div>
            <div class="flex items-center space-x-2">
              <Icon name="mdi:clock-outline" class="w-4 h-4" />
              <span>{{ experience.durationText }}</span>
            </div>
          </div>
          
          <!-- Description -->
          <div v-if="experience.description" class="mb-4">
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">{{ experience.description }}</p>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center justify-end space-x-2 pt-4 border-t border-gray-200 dark:border-gray-700">
            <button
              @click="openEditModal(experience)"
              class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
            >
              <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
              Edit
            </button>
            
            <button
              @click="removeExperience(experience.id!)"
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
    :title="isEditing ? 'Edit Experience' : 'Add Work Experience'"
    size="xl"
    @close="closeModal"
  >
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Experience' : 'Add Work Experience' }}
      </h2>
    </template>
    
    <div class="grid grid-cols-2 gap-6">
      <!-- Job Title -->
      <div>
        <label for="jobTitle" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Title *
        </label>
        <input
          id="jobTitle"
          v-model="formData.jobTitle"
          type="text"
          placeholder="e.g. Senior Software Engineer"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Your official job title or role
        </p>
      </div>

      <!-- Company -->
      <div>
        <label for="company" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Company *
        </label>
        <input
          id="company"
          v-model="formData.company"
          type="text"
          placeholder="e.g. Technology Corp"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Company or organization name
        </p>
      </div>

      <!-- Start Date -->
      <div>
        <label for="startDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Start Date *
        </label>
        <input
          id="startDate"
          v-model="formData.startDate"
          type="date"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          When did you start this position?
        </p>
      </div>

      <!-- End Date / Current Job -->
      <div>
        <label for="endDate" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          End Date
        </label>
        <input
          id="endDate"
          v-model="formData.endDate"
          type="date"
          :disabled="formData.isCurrentJob"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :required="!formData.isCurrentJob"
        />
        <div class="mt-2">
          <label class="flex items-center">
            <input
              v-model="formData.isCurrentJob"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600 text-indigo-600 focus:ring-indigo-500 dark:bg-gray-700"
            />
            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">This is my current job</span>
          </label>
        </div>
      </div>

      <!-- Description -->
      <div class="col-span-2">
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Description
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="6"
          placeholder="Describe your responsibilities, achievements, and key projects. Use bullet points for better readability:&#10;&#10;• Led a team of 5 developers&#10;• Increased system performance by 40%&#10;• Implemented new CI/CD pipeline"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Highlight your key responsibilities, achievements, and impact. Use bullet points for better readability.
        </p>
      </div>

      <!-- Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 col-span-2">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Writing Tips</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li>Use action verbs (led, developed, improved, created)</li>
              <li>Include quantifiable achievements when possible</li>
              <li>Focus on impact and results, not just duties</li>
              <li>Tailor content to be relevant for your target roles</li>
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
        class="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 dark:bg-indigo-500 dark:hover:bg-indigo-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Experience' : 'Save Experience' }}
      </button>
    </template>
  </Modal>
</template>
