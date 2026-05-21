<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useProfileIndexing } from '~/composables/useProfileIndexing'
import { useUserStore } from '~/stores/userStore'
import { useProfileStore } from '~/stores/profileStore'

import SkillsSection from '~/components/profile/skills/SkillsSection.vue'
import ExperienceSection from '~/components/profile/experience/ExperienceSection.vue'
import EducationSection from '~/components/profile/education/EducationSection.vue'
import ProjectSection from '~/components/profile/project/ProjectSection.vue'
import ProfessionalSummarySection from '~/components/profile/professionalSummary/ProfessionalSummarySection.vue'
import BasicInfoSection from '~/components/profile/basicInfo/BasicInfoSection.vue'
import LinksSection from '~/components/profile/links/LinksSection.vue'
import LanguageSection from '~/components/profile/language/LanguageSection.vue'
import CertificationSection from '~/components/profile/certification/CertificationSection.vue'
import CustomSection from '~/components/profile/custom/CustomSection.vue'

// Get user from store
const { user } = useUserStore()

// Route (keep at top-level to ensure it's available in handlers)
const route = useRoute()

// Profile store (use active profile as fallback)
const { activeProfile } = useProfileStore()
// Get indexing composable
const {
  isIndexing,
  indexingStatus,
  indexingError,
  lastIndexedAt,
  startIndexing,
  stopPolling,
  reset: resetIndexing,
  loadLastIndexedTime,
} = useProfileIndexing()

onMounted(() => {
  loadLastIndexedTime()
})

// Profile state for resume generation
const profileData = ref({
  // Basic resume info
  name: '',
  email: '',
  phone: '',
  location: '',
  website: '',
  linkedin: '',
  summary: ''
})

// Form state
const isEditing = ref(false)
const isLoading = ref(false)
const message = ref('')
const errors = ref<Record<string, string>>({})

// Computed
const profileCompletion = computed(() => {
  const fields = Object.values(profileData.value)
  const completed = fields.filter(field => field && field.trim() !== '').length
  return Math.round((completed / fields.length) * 100)
})

// Methods
const handleSave = async () => {
  isLoading.value = true
  errors.value = {}
  message.value = ''

  try {
    // TODO: Implement profile update API call
    await new Promise(resolve => setTimeout(resolve, 1000)) // Mock delay

    message.value = 'Profile updated successfully!'
    isEditing.value = false

    setTimeout(() => {
      message.value = ''
    }, 3000)
  } catch (error: any) {
    errors.value = { general: error.statusMessage || 'Failed to update profile' }
  } finally {
    isLoading.value = false
  }
}

const handleIndex = async () => {
  if (!user.value?.uuid) {
    errors.value = { general: 'User not authenticated' }
    return
  }

  const profileId = (route?.params?.id as string) || activeProfile?.value?.uuid

  if (!profileId) {
    errors.value = { general: 'Profile ID not found. Select or create a profile first.' }
    return
  }

  console.log(`[ProfilePage] handleIndex called for profile ${profileId}`)
  try {
    errors.value = {}
    resetIndexing()
    message.value = ''
    await startIndexing(user.value.uuid, profileId)
  } catch (error: any) {
    console.error(`[ProfilePage] handleIndex error:`, error)
    errors.value = { general: error.message || 'Failed to start indexing' }
  }
}

const handleCancel = () => {
  // Reset form data
  profileData.value = {
    name: '',
    email: '',
    phone: '',
    location: '',
    website: '',
    linkedin: '',
    summary: ''
  }
  isEditing.value = false
  errors.value = {}
}

// Navigation methods
const navigateToSections = () => navigateTo('/profile/sections')
const navigateToExtractResume = () => navigateTo('/profile/extract-resume')
const navigateToLinkedIn = () => navigateTo('/profile/extract-linkedin')
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <!-- Full width container with proper responsive breakpoints -->
    <div class="mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 max-w-none">
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-8">

      <!-- Header -->
      <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div class="flex-1">
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Resume Profile</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">Build your comprehensive profile for AI-powered resume generation.</p>
        </div>
        
        <!-- Index Button -->
        <div class="flex flex-col gap-2">
          <button
            @click="handleIndex"
            :disabled="isIndexing"
            class="px-6 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white font-medium rounded-lg transition-colors duration-200 flex items-center justify-center gap-2 whitespace-nowrap"
          >
            <span v-if="isIndexing" class="inline-block animate-spin">⟳</span>
            <span>{{ isIndexing ? 'Indexing...' : 'Index Profile' }}</span>
          </button>
          
          <!-- Last indexed time -->
          <div v-if="lastIndexedAt" class="text-xs text-gray-500 dark:text-gray-400 text-right">
            Last indexed: {{ lastIndexedAt.toLocaleDateString() }}
          </div>
        </div>
      </div>

      <!-- Success Message -->
      <div v-if="message" class="mb-6 p-4 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 text-green-700 dark:text-green-300 rounded-lg">
        {{ message }}
      </div>

      <!-- Indexing Status Message -->
      <div v-if="indexingStatus && isIndexing" class="mb-6 p-4 bg-blue-100 dark:bg-blue-900/30 border border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300 rounded-lg">
        <div class="flex items-center gap-2">
          <span class="inline-block animate-spin">⟳</span>
          <span>{{ indexingStatus }}</span>
        </div>
      </div>

      <!-- Indexing Success Message -->
      <div v-if="indexingStatus === 'Indexing completed' && !isIndexing" class="mb-6 p-4 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 text-green-700 dark:text-green-300 rounded-lg">
        ✓ {{ indexingStatus }}
      </div>

      <!-- Indexing Error Message -->
      <div v-if="indexingError" class="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg">
        {{ indexingError }}
      </div>

      <!-- Error Message -->
      <div v-if="errors.general" class="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg">
        {{ errors.general }}
      </div>

      <!-- Profile Sections -->
      <div class="space-y-6">
        <!-- Basic Information Section -->
        <BasicInfoSection />
        
        <!-- Professional Summary Section -->
        <ProfessionalSummarySection />
        
        <!-- Links & Social Profiles Section -->
        <LinksSection />
        
        <!-- Other Resume Sections -->
        <ExperienceSection />
        <EducationSection />
        <SkillsSection />
        <ProjectSection />
        <CertificationSection />
        <LanguageSection />
        <CustomSection />
      </div>
          </div>

    </div>
  </div>
</template>

