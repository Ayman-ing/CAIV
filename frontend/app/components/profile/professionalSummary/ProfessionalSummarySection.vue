<script setup lang="ts">
// filepath: frontend/app/components/profile/professionalSummary/ProfessionalSummarySection.vue
import { ref, computed, onMounted } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'
import { useProfileStore } from '~/stores/profileStore'
import { profileSectionsService } from '~/services/profileSectionsService'
import { useToast } from '~/composables/useToast'
import type { ProfessionalSummary } from '~/types/profile'

const profileStore = useProfileStore()
const activeProfile = profileStore.activeProfile
const { success, error } = useToast()

const professionalSummaries = ref<ProfessionalSummary[]>([])
const isExpanded = ref(false)

onMounted(async () => {
  await fetchSummaries()
})

const isLoading = ref(false)
const isModalOpen = ref(false)
const isEditing = ref(false)
const isSaving = ref(false)
const editingSummary = ref<ProfessionalSummary | null>(null)
const maxLength = 500

// Deletion confirmation modal state
const isDeleteModalOpen = ref(false)
const summaryToDelete = ref<ProfessionalSummary | null>(null)
const isDeleting = ref(false)
const isSettingDefault = ref(false)

const formData = ref({
  title: '',
  content: ''
})

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const fetchSummaries = async () => {
  if (!activeProfile.value) return
  isLoading.value = true
  try {
    const data = await profileSectionsService.fetchProfessionalSummaries(activeProfile.value.uuid)
    professionalSummaries.value = data
  } catch (error) {
    console.error('Failed to fetch professional summaries:', error)
  } finally {
    isLoading.value = false
  }
}

const openAddModal = () => {
  isEditing.value = false
  editingSummary.value = null
  formData.value = {
    title: '',
    content: ''
  }
  isModalOpen.value = true
}

const openEditModal = (summary: ProfessionalSummary) => {
  isEditing.value = true
  editingSummary.value = summary
  formData.value = {
    title: summary.title,
    content: summary.content
  }
  isModalOpen.value = true
}

const handleSave = async () => {
  if (!activeProfile.value) return
  isSaving.value = true
  
  try {
    if (isEditing.value && editingSummary.value) {
      await profileSectionsService.updateProfessionalSummary(
        activeProfile.value.uuid,
        editingSummary.value.uuid,
        {
          title: formData.value.title.trim(),
          content: formData.value.content.trim()
        }
      )
      success('Professional summary updated successfully!')
    } else {
      await profileSectionsService.createProfessionalSummary(
        activeProfile.value.uuid,
        {
          title: formData.value.title.trim(),
          content: formData.value.content.trim()
        }
      )
      success('Professional summary added successfully!')
    }
    
    await fetchSummaries()
    closeModal()
  } catch (err) {
    console.error('Failed to save summary', err)
    error(`Failed to save summary: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isSaving.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  editingSummary.value = null
  formData.value = {
    title: '',
    content: ''
  }
}

const openDeleteModal = (summary: ProfessionalSummary) => {
  summaryToDelete.value = summary
  isDeleteModalOpen.value = true
}

const closeDeleteModal = () => {
  isDeleteModalOpen.value = false
  summaryToDelete.value = null
}

const confirmDelete = async () => {
  if (!activeProfile.value || !summaryToDelete.value) return
  
  isDeleting.value = true
  try {
    await profileSectionsService.deleteProfessionalSummary(
      activeProfile.value.uuid,
      summaryToDelete.value.uuid
    )
    // If we reach here without an error, the delete was successful
    await fetchSummaries()
    closeDeleteModal()
    success('Professional summary deleted successfully!')
  } catch (err) {
    console.error('Failed to delete summary:', err)
    error(`Failed to delete summary: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isDeleting.value = false
  }
}

const setAsDefault = async (summary: ProfessionalSummary) => {
  if (!activeProfile.value) return
  
  isSettingDefault.value = true
  try {
    await profileSectionsService.setDefaultProfessionalSummary(
      activeProfile.value.uuid,
      summary.uuid
    )
    await fetchSummaries()
    success('Professional summary set as default!')
  } catch (err) {
    console.error('Failed to set default summary:', err)
    error(`Failed to set default summary: ${err instanceof Error ? err.message : 'Unknown error'}`)
  } finally {
    isSettingDefault.value = false
  }
}



const characterCount = computed(() => formData.value.content.length)
const isOverLimit = computed(() => characterCount.value > maxLength)
const isFormValid = computed(() => 
  formData.value.title.trim() !== '' && 
  formData.value.content.trim() !== '' && 
  !isOverLimit.value
)

const wordCount = computed(() => {
  return formData.value.content.trim() ? formData.value.content.trim().split(/\s+/).length : 0
})

const defaultSummary = computed(() => {
  return professionalSummaries.value[0] // For now first one is default
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
  formData.value.content = template.summary
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
    :is-empty="!isLoading && professionalSummaries.length === 0"
    empty-message="No professional summaries added yet"
    add-button-text="Add Summary"
    @toggle="toggleSection"
    @add="openAddModal"
  >
    <!-- Loading State -->
    <div v-if="isLoading" class="flex justify-center p-8 text-green-600">
      <Icon name="mdi:loading" class="w-8 h-8 animate-spin" />
    </div>

    <!-- Display Mode -->
    <div v-else-if="professionalSummaries.length > 0" class="space-y-6">
      <!-- Summary Stats -->
      <div class="flex items-center justify-between p-4 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
        <div class="flex items-center space-x-4">
          <div class="flex items-center space-x-2">
            <Icon name="mdi:text-box-multiple-outline" class="w-5 h-5 text-green-600 dark:text-green-400" />
            <div>
              <p class="text-sm font-medium text-green-700 dark:text-green-300">Professional Summaries</p>
              <p class="text-xs text-green-600 dark:text-green-400">{{ professionalSummaries.length }} summary{{ professionalSummaries.length !== 1 ? 's' : '' }}</p>
            </div>
          </div>
        </div>
        
        <button
          @click="openAddModal"
          class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:plus" class="w-4 h-4 mr-2" />
          Add Summary
        </button>
      </div>

      <!-- All Summaries List -->
      <div class="space-y-4">
        <div v-for="(summary, index) in professionalSummaries" :key="summary.uuid" class="relative p-6 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-sm hover:shadow-md transition-shadow group">
          <!-- Default Badge -->
          <div v-if="summary.is_default" class="absolute top-4 right-4">
            <span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-300 border border-green-200 dark:border-green-800 rounded-full flex items-center">
              <Icon name="mdi:star" class="w-3 h-3 mr-1" />
              Default
            </span>
          </div>

          <div class="mb-4">
            <h3 class="text-xl font-bold text-gray-900 dark:text-gray-100 mb-1">{{ summary.title }}</h3>
          </div>
          
          <div class="prose dark:prose-invert max-w-none text-gray-700 dark:text-gray-300 whitespace-pre-wrap text-sm leading-relaxed mb-4">
            {{ summary.content }}
          </div>
          
          <div class="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
            <div class="text-xs text-gray-500 dark:text-gray-400">
              {{ summary.content.length }} characters • {{ summary.content.split(/\s+/).length }} words
            </div>
            
            <!-- Action Buttons -->
            <div class="flex items-center space-x-2">
              <button
                @click="openEditModal(summary)"
                class="px-3 py-1.5 text-sm bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors flex items-center"
              >
                <Icon name="mdi:pencil" class="w-4 h-4 mr-1" />
                Edit
              </button>

              <button
                v-if="!summary.is_default"
                @click="setAsDefault(summary)"
                :disabled="isSettingDefault"
                class="px-3 py-1.5 text-sm bg-yellow-50 dark:bg-yellow-900/20 text-yellow-600 dark:text-yellow-400 rounded-lg hover:bg-yellow-100 dark:hover:bg-yellow-900/30 transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Icon v-if="!isSettingDefault" name="mdi:star-outline" class="w-4 h-4 mr-1" />
                <Icon v-else name="mdi:loading" class="w-4 h-4 mr-1 animate-spin" />
                {{ isSettingDefault ? 'Setting...' : 'Set Default' }}
              </button>
              
              <button
                @click="openDeleteModal(summary)"
                class="px-3 py-1.5 text-sm bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors flex items-center"
              >
                <Icon name="mdi:delete" class="w-4 h-4 mr-1" />
                Remove
              </button>
            </div>
          </div>
        </div>
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
            v-model="formData.content"
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
        <div v-if="formData.content.trim()" class="space-y-2">
          <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Preview:</h4>
          <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
            <h5 class="font-medium text-gray-900 dark:text-gray-100 mb-2">{{ formData.title || 'Summary Title' }}</h5>
            <p class="text-gray-900 dark:text-gray-100 leading-relaxed text-sm whitespace-pre-wrap">
              {{ formData.content }}
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
        :disabled="!isFormValid || isSaving"
        class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon v-if="!isSaving" name="mdi:content-save" class="w-4 h-4 mr-2" />
        <Icon v-else name="mdi:loading" class="w-4 h-4 mr-2 animate-spin" />
        {{ isSaving ? 'Saving...' : (isEditing ? 'Update Summary' : 'Add Summary') }}
      </button>
    </template>
  </Modal>

  <!-- Delete Confirmation Modal -->
  <Modal
    v-model="isDeleteModalOpen"
    title="Delete Professional Summary"
    size="sm"
    @close="closeDeleteModal"
  >
    <div class="space-y-4">
      <div class="flex items-start space-x-4">
        <div class="flex-shrink-0">
          <Icon name="mdi:alert-circle" class="w-6 h-6 text-red-600 dark:text-red-400" />
        </div>
        <div class="flex-grow">
          <p class="text-gray-900 dark:text-gray-100 font-medium">Delete Summary?</p>
          <p class="text-gray-600 dark:text-gray-400 text-sm mt-1">
            Are you sure you want to delete <span class="font-semibold">{{ summaryToDelete?.title }}</span>? This action cannot be undone.
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