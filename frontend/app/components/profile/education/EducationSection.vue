<script setup lang="ts">
// filepath: frontend/app/components/profile/education/EducationSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import type { Education, EducationFormData, EducationDisplay } from './types'

// Education Data
const educationList = ref<Education[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingEducation = ref<Education | null>(null)

// Form state
const formData = ref<EducationFormData>({
  institution: '',
  degree: '',
  fieldOfStudy: '',
  honors: '',
  gpa: '',
  startDate: '',
  endDate: '',
  description: '',
  isOngoing: false
})

// Predefined options
const degreeTypes = [
  'Associate Degree', 'Bachelor\'s Degree', 'Master\'s Degree', 'Doctoral Degree', 'PhD',
  'Certificate', 'Diploma', 'Professional Certification', 'Online Course', 'Bootcamp', 'Other'
]

const gpaScales = [
  { value: '4.0', label: '4.0 Scale' },
  { value: '5.0', label: '5.0 Scale' },
  { value: '10.0', label: '10.0 Scale' },
  { value: '100', label: '100 Point Scale' },
  { value: 'percentage', label: 'Percentage (%)' }
]

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingEducation.value = null
  formData.value = {
    institution: '',
    degree: '',
    fieldOfStudy: '',
    honors: '',
    gpa: '',
    startDate: '',
    endDate: '',
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
    fieldOfStudy: education.fieldOfStudy,
    honors: education.honors || '',
    gpa: education.gpa?.toString() || '',
    startDate: education.startDate,
    endDate: education.endDate || '',
    description: education.description || '',
    isOngoing: !education.endDate
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingEducation.value) {
    // Update existing education
    const index = educationList.value.findIndex(edu => edu.id === editingEducation.value!.id)
    if (index !== -1 && educationList.value[index]) {
      educationList.value[index] = {
        ...educationList.value[index],
        institution: formData.value.institution.trim(),
        degree: formData.value.degree.trim(),
        fieldOfStudy: formData.value.fieldOfStudy.trim(),
        honors: formData.value.honors.trim() || undefined,
        gpa: formData.value.gpa ? parseFloat(formData.value.gpa) : undefined,
        startDate: formData.value.startDate,
        endDate: formData.value.isOngoing ? undefined : formData.value.endDate,
        description: formData.value.description.trim() || undefined
      }
    }
  } else {
    // Add new education
    const newEducation: Education = {
      id: Date.now(),
      institution: formData.value.institution.trim(),
      degree: formData.value.degree.trim(),
      fieldOfStudy: formData.value.fieldOfStudy.trim(),
      honors: formData.value.honors.trim() || undefined,
      gpa: formData.value.gpa ? parseFloat(formData.value.gpa) : undefined,
      startDate: formData.value.startDate,
      endDate: formData.value.isOngoing ? undefined : formData.value.endDate,
      description: formData.value.description.trim() || undefined,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    }
    educationList.value.push(newEducation)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingEducation.value = null
  formData.value = {
    institution: '',
    degree: '',
    fieldOfStudy: '',
    honors: '',
    gpa: '',
    startDate: '',
    endDate: '',
    description: '',
    isOngoing: false
  }
}

const removeEducation = (id: number) => {
  const index = educationList.value.findIndex(edu => edu.id === id)
  if (index !== -1) {
    educationList.value.splice(index, 1)
  }
}

const isFormValid = computed(() => {
  return formData.value.institution.trim() !== '' && 
         formData.value.degree.trim() !== '' && 
         formData.value.fieldOfStudy.trim() !== '' &&
         formData.value.startDate !== '' &&
         (formData.value.isOngoing || formData.value.endDate !== '')
})

const hasEducation = computed(() => {
  return educationList.value.length > 0
})

// Enhanced display data
const displayEducation = computed((): EducationDisplay[] => {
  return educationList.value.map(edu => {
    const startDate = new Date(edu.startDate)
    const endDate = edu.endDate ? new Date(edu.endDate) : null
    
    const formatDate = (dateStr: string) => {
      const date = new Date(dateStr)
      return date.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
    
    return {
      ...edu,
      displayDateRange: `${formatDate(edu.startDate)} - ${edu.endDate ? formatDate(edu.endDate) : 'Present'}`,
      isCompleted: !!edu.endDate,
      completionYear: endDate?.getFullYear()
    } as EducationDisplay
  }).sort((a, b) => new Date(b.startDate).getTime() - new Date(a.startDate).getTime())
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
    :is-empty="!hasEducation"
    empty-message="Add your education"
    add-button-text="Add Education"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="hasEducation" class="space-y-6">
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
        <div v-for="education in displayEducation" :key="education.id" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow">
          <!-- Ongoing Badge -->
          <div v-if="!education.isCompleted" class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 border border-blue-200 dark:border-blue-800 rounded-full">
              In Progress
            </span>
          </div>
          
          <!-- Degree & Field -->
          <div class="mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-1">
              {{ education.degree }}{{ education.fieldOfStudy ? ` in ${education.fieldOfStudy}` : '' }}
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
            <p class="text-gray-700 dark:text-gray-300 whitespace-pre-wrap leading-relaxed">{{ education.description }}</p>
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
              @click="removeEducation(education.id!)"
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
      <div>
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
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          School, university, or educational institution
        </p>
      </div>

      <!-- Degree -->
      <div>
        <label for="degree" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Degree *
        </label>
        <select
          id="degree"
          v-model="formData.degree"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        >
          <option value="">Select degree type</option>
          <option v-for="degree in degreeTypes" :key="degree" :value="degree">
            {{ degree }}
          </option>
        </select>
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Type of degree or qualification
        </p>
      </div>

      <!-- Field of Study -->
      <div>
        <label for="fieldOfStudy" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Field of Study *
        </label>
        <input
          id="fieldOfStudy"
          v-model="formData.fieldOfStudy"
          type="text"
          placeholder="e.g. Computer Science, Business Administration"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Your major, specialization, or area of study
        </p>
      </div>

      <!-- GPA -->
      <div>
        <label for="gpa" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          GPA (Optional)
        </label>
        <input
          id="gpa"
          v-model="formData.gpa"
          type="number"
          step="0.01"
          placeholder="e.g. 3.75"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Only include if above average (3.5+ on 4.0 scale)
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
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          When did you start this program?
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
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
          :required="!formData.isOngoing"
        />
        <div class="mt-2">
          <label class="flex items-center">
            <input
              v-model="formData.isOngoing"
              type="checkbox"
              class="rounded border-gray-300 dark:border-gray-600 text-green-600 focus:ring-green-500 dark:bg-gray-700"
            />
            <span class="ml-2 text-sm text-gray-700 dark:text-gray-300">Currently enrolled</span>
          </label>
        </div>
      </div>

      <!-- Honors -->
      <div class="col-span-2">
        <label for="honors" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Honors & Awards (Optional)
        </label>
        <input
          id="honors"
          v-model="formData.honors"
          type="text"
          placeholder="e.g. Magna Cum Laude, Dean's List, Honor Society"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Academic honors, awards, or distinctions received
        </p>
      </div>

      <!-- Description -->
      <div class="col-span-2">
        <label for="description" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Description (Optional)
        </label>
        <textarea
          id="description"
          v-model="formData.description"
          rows="4"
          placeholder="Relevant coursework, projects, thesis, or other details..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Relevant coursework, thesis, notable projects, or achievements
        </p>
      </div>

      <!-- Guidelines -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4 col-span-2">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Education Tips</p>
            <ul class="text-xs space-y-1 list-disc list-inside">
              <li>List education in reverse chronological order</li>
              <li>Only include GPA if it's impressive (3.5+ on 4.0 scale)</li>
              <li>Mention relevant coursework for early career professionals</li>
              <li>Include honors and awards to stand out</li>
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
        class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Education' : 'Save Education' }}
      </button>
    </template>
  </Modal>
</template>
