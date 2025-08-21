<script setup lang="ts">
// filepath: frontend/app/components/profile/basicInfo/BasicInfoSection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'

interface BasicInfo {
  fullName: string
  email: string
  phoneNumber: string
  location: string
}

// Basic Information Data
const basicInfo = ref<BasicInfo>({
  fullName: '',
  email: '',
  phoneNumber: '',
  location: ''
})

const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)

// Form state
const formData = ref<BasicInfo>({
  fullName: '',
  email: '',
  phoneNumber: '',
  location: ''
})

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openEditModal = () => {
  formData.value = { ...basicInfo.value }
  isModalOpen.value = true
}

const handleSave = () => {
  basicInfo.value = { ...formData.value }
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  formData.value = {
    fullName: '',
    email: '',
    phoneNumber: '',
    location: ''
  }
}

const isFormValid = computed(() => {
  return formData.value.fullName.trim() !== '' && 
         formData.value.phoneNumber.trim() !== '' && 
         formData.value.location.trim() !== ''
})

const completionFields = computed(() => {
  const fields = [
    { key: 'fullName', label: 'Full Name', value: basicInfo.value.fullName, required: true },
    { key: 'email', label: 'Email', value: basicInfo.value.email, required: false },
    { key: 'phoneNumber', label: 'Phone Number', value: basicInfo.value.phoneNumber, required: true },
    { key: 'location', label: 'Location', value: basicInfo.value.location, required: true }
  ]
  return fields
})

const completionPercentage = computed(() => {
  const completed = completionFields.value.filter(field => field.value.trim() !== '').length
  return Math.round((completed / completionFields.value.length) * 100)
})

const hasRequiredFields = computed(() => {
  return basicInfo.value.fullName && basicInfo.value.phoneNumber && basicInfo.value.location
})
</script>

<template>
  <CollapsibleSection
    title="Basic Information"
    description="Your personal contact information"
    icon="mdi:account-circle"
    icon-color="text-blue-600 dark:text-blue-400"
    icon-bg-color="bg-blue-100 dark:bg-blue-900/30"
    button-color="bg-blue-600 dark:bg-blue-500 hover:bg-blue-700 dark:hover:bg-blue-600"
    :is-expanded="isExpanded"
    :is-empty="!hasRequiredFields"
    empty-message="Complete your basic information"
    add-button-text="Add Information"
    @toggle="toggleSection"
    @add="openEditModal"
  >
    <!-- Display Mode -->
    <div v-if="hasRequiredFields" class="space-y-4">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div v-for="field in completionFields" :key="field.key" class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
          <div class="flex items-center justify-between mb-1">
            <label class="text-sm font-medium text-gray-700 dark:text-gray-300">
              {{ field.label }}
              <span v-if="field.required" class="text-red-500">*</span>
            </label>
            <Icon 
              v-if="field.value.trim()"
              name="mdi:check-circle" 
              class="w-4 h-4 text-green-500 dark:text-green-400" 
            />
          </div>
          <p class="text-gray-900 dark:text-gray-100 font-medium">
            {{ field.value || 'Not specified' }}
          </p>
        </div>
      </div>

      <!-- Completion Status -->
      <div class="flex items-center justify-between p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
        <div class="flex items-center space-x-3">
          <div class="relative w-8 h-8">
            <svg class="w-8 h-8 transform -rotate-90" viewBox="0 0 36 36">
              <path
                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                stroke-dasharray="100, 100"
                class="text-gray-300 dark:text-gray-600"
              />
              <path
                d="M18 2.0845
                  a 15.9155 15.9155 0 0 1 0 31.831
                  a 15.9155 15.9155 0 0 1 0 -31.831"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
                :stroke-dasharray="`${completionPercentage}, 100`"
                class="text-blue-600 dark:text-blue-400"
              />
            </svg>
            <div class="absolute inset-0 flex items-center justify-center">
              <span class="text-xs font-semibold text-blue-600 dark:text-blue-400">{{ completionPercentage }}%</span>
            </div>
          </div>
          <div>
            <p class="text-sm font-medium text-blue-700 dark:text-blue-300">Profile Completion</p>
            <p class="text-xs text-blue-600 dark:text-blue-400">{{ completionFields.filter(f => f.value.trim()).length }}/{{ completionFields.length }} fields completed</p>
          </div>
        </div>
        
        <button
          @click="openEditModal"
          class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:pencil" class="w-4 h-4 mr-2" />
          Edit Information
        </button>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Edit Modal -->
  <Modal
    v-model="isModalOpen"
    title="Basic Information"
    size="xl"
    @close="closeModal"
  >
  <template #header>
    <h2 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Basic Information</h2>
  </template>
    <div class="grid grid-cols-2 gap-8">
      <!-- Full Name -->

      <div>
        <label for="fullName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Full Name *
        </label>
        <input
          id="fullName"
          v-model="formData.fullName"
          type="text"
          placeholder="Enter your full name"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          This will appear on your resumes and professional documents
        </p>
      </div>

      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Email Address
        </label>
        <input
          id="email"
          v-model="formData.email"
          type="email"
          placeholder="your.email@example.com"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Optional - Professional email for resume contact information
        </p>
      </div>

      <!-- Phone Number -->
      <div>
        <label for="phoneNumber" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Phone Number *
        </label>
        <input
          id="phoneNumber"
          v-model="formData.phoneNumber"
          type="tel"
          placeholder="+1 (555) 123-4567"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Include country code for international numbers
        </p>
      </div>

      <!-- Location -->
      <div>
        <label for="location" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Location *
        </label>
        <input
          id="location"
          v-model="formData.location"
          type="text"
          placeholder="City, State/Province, Country"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100"
          required
        />
        <p class="mt-1 text-xs text-gray-500 dark:text-gray-400">
          Include city and country at minimum
        </p>
      </div>

      <!-- Privacy Notice -->
      <div class="bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg p-3 col-span-2">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:shield-account" class="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-amber-700 dark:text-amber-300">
            <p class="font-medium mb-1">Privacy & Security</p>
            <p class="text-xs">Your personal information is stored securely and will only be used in the resumes you generate. We never share your data with third parties.</p>
          </div>
        </div>
      </div>

      <!-- Preview -->
      <div v-if="formData.fullName" class="space-y-2 col-span-2">
        <h4 class="text-sm font-medium text-gray-700 dark:text-gray-300">Preview:</h4>
        <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg border border-gray-200 dark:border-gray-600">
          <div class="text-center">
            <h3 class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ formData.fullName }}</h3>
            <div class="flex flex-wrap justify-center gap-2 mt-2 text-sm text-gray-600 dark:text-gray-400">
              <span v-if="formData.email">{{ formData.email }}</span>
              <span v-if="formData.email && formData.phoneNumber">•</span>
              <span v-if="formData.phoneNumber">{{ formData.phoneNumber }}</span>
              <span v-if="(formData.email || formData.phoneNumber) && formData.location">•</span>
              <span v-if="formData.location">{{ formData.location }}</span>
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
        class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors flex items-center disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon name="mdi:content-save" class="w-4 h-4 mr-2" />
        Save Information
      </button>
    </template>
  </Modal>
</template>