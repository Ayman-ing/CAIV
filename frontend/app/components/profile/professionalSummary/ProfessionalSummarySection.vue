<script setup lang="ts">
// filepath: frontend/app/components/profile/professionalSummary/ProfessionalSummarySection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'

interface ProfessionalSummary {
  id: string
  title: string
  summary: string
  isDefault: boolean
  createdAt: string
}

// Professional Summary Data
const professionalSummaries = ref<ProfessionalSummary[]>([])
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)
const isEditing = ref(false)
const editingSummary = ref<ProfessionalSummary | null>(null)

// Form state
const formData = ref({
  title: '',
  summary: ''
})

const maxLength = 500

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openAddModal = () => {
  isEditing.value = false
  editingSummary.value = null
  formData.value = {
    title: '',
    summary: ''
  }
  isModalOpen.value = true
}

const openEditModal = (summary: ProfessionalSummary) => {
  isEditing.value = true
  editingSummary.value = summary
  formData.value = {
    title: summary.title,
    summary: summary.summary
  }
  isModalOpen.value = true
}

const handleSave = () => {
  if (isEditing.value && editingSummary.value) {
    // Update existing summary
    const index = professionalSummaries.value.findIndex(s => s.id === editingSummary.value!.id)
    if (index !== -1 && professionalSummaries.value[index]) {
      professionalSummaries.value[index] = {
        id: professionalSummaries.value[index].id,
        title: formData.value.title.trim(),
        summary: formData.value.summary.trim(),
        isDefault: professionalSummaries.value[index].isDefault,
        createdAt: professionalSummaries.value[index].createdAt
      }
    }
  } else {
    // Add new summary
    const newSummary: ProfessionalSummary = {
      id: Date.now().toString(),
      title: formData.value.title.trim(),
      summary: formData.value.summary.trim(),
      isDefault: professionalSummaries.value.length === 0, // First summary is default
      createdAt: new Date().toISOString()
    }
    professionalSummaries.value.push(newSummary)
  }
  
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  editingSummary.value = null
  formData.value = {
    title: '',
    summary: ''
  }
}

const removeSummary = (id: string) => {
  const summaryToRemove = professionalSummaries.value.find(s => s.id === id)
  if (summaryToRemove?.isDefault && professionalSummaries.value.length > 1) {
    // If removing default summary, make the first remaining one default
    const remainingSummaries = professionalSummaries.value.filter(s => s.id !== id)
    if (remainingSummaries.length > 0) {
      if (remainingSummaries[0]) {
        remainingSummaries[0].isDefault = true
      }
    }
  }
  professionalSummaries.value = professionalSummaries.value.filter(s => s.id !== id)
}

const setAsDefault = (id: string) => {
  professionalSummaries.value.forEach(summary => {
    summary.isDefault = summary.id === id
  })
}

const duplicateSummary = (summary: ProfessionalSummary) => {
  const newSummary: ProfessionalSummary = {
    id: Date.now().toString(),
    title: `${summary.title} (Copy)`,
    summary: summary.summary,
    isDefault: false,
    createdAt: new Date().toISOString()
  }
  professionalSummaries.value.push(newSummary)
}

const characterCount = computed(() => formData.value.summary.length)
const isOverLimit = computed(() => characterCount.value > maxLength)
const isFormValid = computed(() => 
  formData.value.title.trim() !== '' && 
  formData.value.summary.trim() !== '' && 
  !isOverLimit.value
)

const wordCount = computed(() => {
  return formData.value.summary.trim() ? formData.value.summary.trim().split(/\s+/).length : 0
})

const defaultSummary = computed(() => {
  return professionalSummaries.value.find(s => s.isDefault)
})

// Predefined summary templates for quick start
const summaryTemplates = [
  {
    title: 'Software Engineer',
    summary: 'Experienced software engineer with [X] years in full-stack development. Proven track record of delivering scalable web applications using modern technologies. Passionate about creating user-centric solutions and leading cross-functional teams.'
  },
  {
    title: 'Marketing Professional',
    summary: 'Results-driven marketing professional with expertise in digital marketing, brand strategy, and campaign management. Successfully increased brand awareness and drove revenue growth across multiple industries.'
  },
  {
    title: 'Project Manager',
    summary: 'Certified project manager with [X] years of experience leading cross-functional teams and delivering complex projects on time and within budget. Expert in Agile methodologies and stakeholder management.'
  }
]

const useTemplate = (template: any) => {
  formData.value.title = template.title
  formData.value.summary = template.summary
}
</script>

<template>
  <CollapsibleSection
    title="Professional Summaries"
    description="Multiple professional summaries for different career focuses"
    icon="mdi:text-box-multiple-outline"
    icon-color="text-green-600 dark:text-green-400"
    icon-bg-color="bg-green-100 dark:bg-green-900/30"
    button-color="bg-green-600 dark:bg-green-500 hover:bg-green-700 dark:hover:bg-green-600"
    :is-expanded="isExpanded"
    :is-empty="professionalSummaries.length === 0"
    empty-message="No professional summaries added yet"
    add-button-text="Add Summary"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Display Mode -->
    <div v-if="professionalSummaries.length > 0" class="space-y-4">
      <!-- Default Summary Highlight -->
      <div v-if="defaultSummary" class="p-4 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg">
        <div class="flex items-center justify-between mb-2">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:star" class="w-5 h-5 text-green-600 dark:text-green-400" />
            <span class="text-sm font-medium text-green-700 dark:text-green-300">Default Summary</span>
          </div>
          <span class="text-xs text-green-600 dark:text-green-400 bg-green-100 dark:bg-green-900/40 px-2 py-1 rounded-full">
            {{ defaultSummary.title }}
          </span>
        </div>
        <p class="text-green-900 dark:text-green-100 text-sm leading-relaxed">
          {{ defaultSummary.summary }}
        </p>
      </div>

      <!-- All Summaries List -->
      <div class="space-y-3">
        <div v-for="summary in professionalSummaries" :key="summary.id" class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600 group hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors">
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center space-x-2">
              <Icon 
                name="mdi:star" 
                class="w-4 h-4"
                :class="summary.isDefault ? 'text-green-500' : 'text-gray-300 dark:text-gray-600'"
              />
              <h4 class="font-medium text-gray-900 dark:text-gray-100">{{ summary.title }}</h4>
              <span v-if="summary.isDefault" class="text-xs bg-green-100 dark:bg-green-900/40 text-green-600 dark:text-green-400 px-2 py-1 rounded-full">
                Default
              </span>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex items-center space-x-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <button
                v-if="!summary.isDefault"
                @click="setAsDefault(summary.id)"
                class="p-2 text-gray-500 hover:text-green-600 dark:hover:text-green-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
                title="Set as default"
              >
                <Icon name="mdi:star-outline" class="w-4 h-4" />
              </button>
              
              <button
                @click="duplicateSummary(summary)"
                class="p-2 text-gray-500 hover:text-blue-600 dark:hover:text-blue-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
                title="Duplicate summary"
              >
                <Icon name="mdi:content-copy" class="w-4 h-4" />
              </button>
              
              <button
                @click="openEditModal(summary)"
                class="p-2 text-gray-500 hover:text-green-600 dark:hover:text-green-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors"
                title="Edit summary"
              >
                <Icon name="mdi:pencil" class="w-4 h-4" />
              </button>
              
              <button
                @click="removeSummary(summary.id)"
                :disabled="professionalSummaries.length === 1"
                class="p-2 text-gray-500 hover:text-red-600 dark:hover:text-red-400 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-md transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                title="Remove summary"
              >
                <Icon name="mdi:trash-can" class="w-4 h-4" />
              </button>
            </div>
          </div>
          
          <p class="text-gray-700 dark:text-gray-300 text-sm leading-relaxed mb-2">
            {{ summary.summary }}
          </p>
          
          <div class="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{{ summary.summary.length }} characters • {{ summary.summary.split(/\s+/).length }} words</span>
            <span>Created {{ new Date(summary.createdAt).toLocaleDateString() }}</span>
          </div>
        </div>
      </div>

      <!-- Add Another Button -->
      <div class="flex justify-center pt-3 border-t border-gray-200 dark:border-gray-700">
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Another Summary
        </button>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Add/Edit Modal -->
  <Modal
    v-model="isModalOpen"
    :title="isEditing ? 'Edit Professional Summary' : 'Add Professional Summary'"
    size="full"
    @close="closeModal"
  >
    <template #header>
      <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">
        {{ isEditing ? 'Edit Professional Summary' : 'Add Professional Summary' }}
      </h2>
    </template>

    <div class="grid grid-cols-3 gap-8">
      <!-- Form Section -->
      <div class="col-span-2 space-y-4">
        <!-- Title -->
        <div>
          <label for="summaryTitle" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Summary Title *
          </label>
          <input
            id="summaryTitle"
            v-model="formData.title"
            type="text"
            placeholder="e.g., Software Engineer, Marketing Professional, Project Manager"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
            required
          />
          <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
            Give this summary a descriptive name for easy identification
          </p>
        </div>

        <!-- Summary Text -->
        <div>
          <label for="summary" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Professional Summary *
          </label>
          <textarea
            id="summary"
            v-model="formData.summary"
            rows="8"
            :maxlength="maxLength"
            placeholder="Write a compelling summary of your professional background, key skills, and career objectives..."
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
            :class="{ 'border-red-500 dark:border-red-400': isOverLimit }"
          ></textarea>
          
          <!-- Character and Word Count -->
          <div class="flex justify-between items-center mt-2 text-sm">
            <div class="text-gray-500 dark:text-gray-400">
              {{ wordCount }} words
            </div>
            <div :class="isOverLimit ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'">
              {{ characterCount }}/{{ maxLength }} characters
            </div>
          </div>
        </div>

        <!-- Preview -->
        <div v-if="formData.summary.trim()" class="space-y-2">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Preview:</h4>
          <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
            <h5 class="font-medium text-gray-900 dark:text-gray-100 mb-2">{{ formData.title || 'Summary Title' }}</h5>
            <p class="text-gray-900 dark:text-gray-100 leading-relaxed text-sm whitespace-pre-wrap">
              {{ formData.summary }}
            </p>
          </div>
        </div>
      </div>

      <!-- Templates & Tips Section -->
      <div class="space-y-4">
        <!-- Quick Templates -->
        <div v-if="!isEditing" class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-4">
          <h4 class="text-sm font-medium text-blue-700 dark:text-blue-300 mb-3 flex items-center">
            <Icon name="mdi:lightning-bolt" class="w-4 h-4 mr-2" />
            Quick Templates
          </h4>
          <div class="space-y-2">
            <button
              v-for="template in summaryTemplates"
              :key="template.title"
              @click="useTemplate(template)"
              class="w-full text-left p-2 text-xs bg-white dark:bg-blue-900/30 border border-blue-200 dark:border-blue-700 rounded-md hover:bg-blue-50 dark:hover:bg-blue-900/40 transition-colors"
            >
              <div class="font-medium text-blue-700 dark:text-blue-300">{{ template.title }}</div>
              <div class="text-blue-600 dark:text-blue-400 mt-1 truncate">{{ template.summary.substring(0, 60) }}...</div>
            </button>
          </div>
        </div>

        <!-- Tips -->
        <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-4">
          <div class="flex items-start space-x-2">
            <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5 flex-shrink-0" />
            <div class="text-sm text-amber-700 dark:text-amber-300">
              <p class="font-medium mb-2">Writing Tips:</p>
              <ul class="space-y-1 text-xs">
                <li>• Include years of experience</li>
                <li>• Mention key skills and technologies</li>
                <li>• Highlight major achievements</li>
                <li>• Keep it concise (2-4 sentences)</li>
                <li>• Tailor for different job types</li>
              </ul>
            </div>
          </div>
        </div>

        <!-- Usage Info -->
        <div class="bg-gray-50 dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-4">
          <div class="flex items-start space-x-2">
            <Icon name="mdi:information-outline" class="w-5 h-5 text-gray-600 dark:text-gray-400 mt-0.5 flex-shrink-0" />
            <div class="text-sm text-gray-700 dark:text-gray-300">
              <p class="font-medium mb-2">Multiple Summaries:</p>
              <p class="text-xs">Create different summaries for various career focuses. Mark one as default for quick resume generation.</p>
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
        class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        {{ isEditing ? 'Update Summary' : 'Add Summary' }}
      </button>
    </template>
  </Modal>
</template>