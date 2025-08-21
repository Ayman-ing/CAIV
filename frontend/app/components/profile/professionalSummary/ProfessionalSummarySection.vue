<script setup lang="ts">
// filepath: frontend/app/components/profile/professionalSummary/ProfessionalSummarySection.vue
import { ref, computed } from 'vue'
import CollapsibleSection from '~/components/ui/CollapsibleSection.vue'
import Modal from '~/components/ui/Modal.vue'

// Professional Summary Data
const professionalSummary = ref('')
const isExpanded = ref(false)

// Modal state
const isModalOpen = ref(false)

// Form state
const formData = ref('')
const maxLength = 500

const toggleSection = () => {
  isExpanded.value = !isExpanded.value
}

const openEditModal = () => {
  formData.value = professionalSummary.value
  isModalOpen.value = true
}

const handleSave = () => {
  professionalSummary.value = formData.value.trim()
  closeModal()
}

const closeModal = () => {
  isModalOpen.value = false
  formData.value = ''
}

const characterCount = computed(() => formData.value.length)
const isOverLimit = computed(() => characterCount.value > maxLength)
const isFormValid = computed(() => formData.value.trim() !== '' && !isOverLimit.value)

const wordCount = computed(() => {
  return formData.value.trim() ? formData.value.trim().split(/\s+/).length : 0
})
</script>

<template>
  <CollapsibleSection
    title="Professional Summary"
    description="A brief overview of your professional background and key strengths"
    icon="mdi:text-box-outline"
    icon-color="text-green-600 dark:text-green-400"
    icon-bg-color="bg-green-100 dark:bg-green-900/30"
    button-color="bg-green-600 dark:bg-green-500 hover:bg-green-700 dark:hover:bg-green-600"
    :is-expanded="isExpanded"
    :is-empty="!professionalSummary"
    empty-message="No professional summary added yet"
    add-button-text="Add Summary"
    @toggle="toggleSection"
    @add="openEditModal"
  >
    <!-- Display Mode -->
    <div v-if="professionalSummary" class="space-y-4">
      <div class="bg-gray-50 dark:bg-gray-700 border border-gray-200 dark:border-gray-600 rounded-lg p-4">
        <p class="text-gray-900 dark:text-gray-100 leading-relaxed whitespace-pre-wrap">
          {{ professionalSummary }}
        </p>
      </div>

      <div class="flex justify-between items-center text-sm text-gray-500 dark:text-gray-400">
        <span>{{ professionalSummary.length }} characters • {{ professionalSummary.trim().split(/\s+/).length }} words</span>
        <button
          @click="openEditModal"
          class="px-4 py-2 bg-green-600 hover:bg-green-700 dark:bg-green-500 dark:hover:bg-green-600 text-white rounded-lg transition-colors flex items-center"
        >
          <Icon name="mdi:pencil" class="w-4 h-4 mr-2" />
          Edit Summary
        </button>
      </div>
    </div>
  </CollapsibleSection>

  <!-- Edit Modal -->
  <Modal
    v-model="isModalOpen"
    title="Professional Summary"
    size="full"
    @close="closeModal"
  >
    <div class="space-y-4">
      <div>
        <label for="summary" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Professional Summary *
        </label>
        <textarea
          id="summary"
          v-model="formData"
          rows="8"
          :maxlength="maxLength"
          placeholder="Write a compelling summary of your professional background, key skills, and career objectives. This will be used across all your generated resumes.

Example: 'Experienced software engineer with 5+ years in full-stack development. Proven track record of delivering scalable web applications using React, Node.js, and cloud technologies. Passionate about creating user-centric solutions and leading cross-functional teams.'"
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 resize-none"
          :class="{ 'border-red-500 dark:border-red-400': isOverLimit }"
        ></textarea>
      </div>

      <!-- Character and Word Count -->
      <div class="flex justify-between items-center text-sm">
        <div class="text-gray-500 dark:text-gray-400">
          {{ wordCount }} words
        </div>
        <div :class="isOverLimit ? 'text-red-600 dark:text-red-400' : 'text-gray-500 dark:text-gray-400'">
          {{ characterCount }}/{{ maxLength }} characters
        </div>
      </div>

      <!-- Tips -->
      <div class="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg p-3">
        <div class="flex items-start space-x-2">
          <Icon name="mdi:lightbulb-outline" class="w-5 h-5 text-blue-600 dark:text-blue-400 mt-0.5 flex-shrink-0" />
          <div class="text-sm text-blue-700 dark:text-blue-300">
            <p class="font-medium mb-1">Tips for a great professional summary:</p>
            <ul class="space-y-1 text-xs">
              <li>• Include your years of experience and key skills</li>
              <li>• Mention specific technologies or industries</li>
              <li>• Highlight your most impressive achievements</li>
              <li>• Keep it concise but compelling (2-4 sentences)</li>
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
        Save Summary
      </button>
    </template>
  </Modal>
</template>