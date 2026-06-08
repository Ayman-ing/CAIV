<script setup lang="ts">
import { ref, computed, onUnmounted, provide, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useProfileIndexing } from '~/composables/useProfileIndexing'
import { useIndexingStatus } from '~/composables/useIndexingStatus'
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

const { user } = useUserStore()
const route = useRoute()
const { activeProfile } = useProfileStore()

// Indexing composables
const {
  isIndexing,
  indexingStatus,
  indexingError,
  indexingProgress,
  indexingTotal,
  indexingPhase,
  indexingSkipped,
  indexingSection,
  progressPercent,
  progressLabel,
  lastIndexedAt,
  startIndexing,
  reset: resetIndexing,
  onEntityIndexed,
  connectPersistentSSE,
} = useProfileIndexing()

const indexingStatusInstance = useIndexingStatus()
const {
  refreshStatus,
  reindexEntity,
  getStatus,
  markEntityAsIndexed,
  summary,
} = indexingStatusInstance

// Provide indexing status to child section components
provide('indexingStatus', indexingStatusInstance)

const profileId = computed(() => (route?.params?.id as string) || activeProfile?.value?.uuid)

// Load status + connect SSE when profile ID becomes available
watch([profileId, user], async ([newId]) => {
  if (newId && user.value?.uuid) {
    await refreshStatus(newId)
    connectPersistentSSE(newId, user.value.uuid)
  }
}, { immediate: true })

// Disconnect SSE on unmount
onUnmounted(() => {
  resetIndexing()
})

// Wire up per-entity SSE events to update status in real-time
onEntityIndexed((entityUuid, _section, status) => {
  if (status === 'completed' || status === 'skipped') {
    markEntityAsIndexed(entityUuid)
  }
})

// Profile state
const profileData = ref({
  name: '',
  email: '',
  phone: '',
  location: '',
  website: '',
  linkedin: '',
  summary: ''
})

const isEditing = ref(false)
const isLoading = ref(false)
const message = ref('')
const errors = ref<Record<string, string>>({})

const profileCompletion = computed(() => {
  const fields = Object.values(profileData.value)
  const completed = fields.filter(field => field && field.trim() !== '').length
  return Math.round((completed / fields.length) * 100)
})

const handleSave = async () => {
  isLoading.value = true
  errors.value = {}
  message.value = ''

  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
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

  const id = profileId.value
  if (!id) {
    errors.value = { general: 'Profile ID not found. Select or create a profile first.' }
    return
  }

  try {
    errors.value = {}
    resetIndexing()
    message.value = ''
    await startIndexing(user.value.uuid, id)
  } catch (error: any) {
    errors.value = { general: error.message || 'Failed to start indexing' }
  }
}

const handleCancel = () => {
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

const navigateToSections = () => navigateTo('/profile/sections')
const navigateToExtractResume = () => navigateTo('/profile/extract-resume')
const navigateToLinkedIn = () => navigateTo('/profile/extract-linkedin')

// On indexing complete, refresh status
watch(isIndexing, async (indexing) => {
  if (!indexing && profileId.value && user.value?.uuid) {
    await refreshStatus(profileId.value)
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 max-w-none">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-8">

        <!-- Header -->
        <div class="mb-8 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
          <div class="flex-1">
            <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Resume Profile</h1>
            <p class="text-gray-600 dark:text-gray-400 mt-2">
              Build your comprehensive profile for AI-powered resume generation.
              <span v-if="summary.total > 0" class="text-sm">
                — <span class="text-green-600 dark:text-green-400">{{ summary.indexed }}</span> indexed,
                <span class="text-amber-600 dark:text-amber-400">{{ summary.needsReindex }}</span> needs reindex,
                <span class="text-gray-400">{{ summary.neverIndexed }}</span> not indexed
              </span>
            </p>
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

            <div v-if="lastIndexedAt" class="text-xs text-gray-500 dark:text-gray-400 text-right">
              Last indexed: {{ lastIndexedAt.toLocaleDateString() }}
            </div>
          </div>
        </div>

        <!-- Success Message -->
        <div v-if="message" class="mb-6 p-4 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 text-green-700 dark:text-green-300 rounded-lg">
          {{ message }}
        </div>

        <!-- Progress Bar -->
        <div v-if="isIndexing && indexingTotal > 0" class="mb-6">
          <div class="flex items-center justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
            <div class="flex items-center gap-2">
              <span v-if="indexingPhase === 'embedding'" class="inline-block animate-spin">⟳</span>
              <span>{{ progressLabel }}</span>
              <span v-if="indexingSkipped > 0 && indexingPhase === 'analyzing'" class="text-gray-400">
                ({{ indexingSkipped }} unchanged)
              </span>
            </div>
            <div class="flex items-center gap-3">
              <span v-if="indexingSkipped > 0 && indexingPhase === 'persisting'" class="text-gray-400">
                {{ indexingSkipped }} unchanged
              </span>
              <span>{{ progressPercent }}%</span>
            </div>
          </div>
          <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2.5">
            <div
              class="bg-indigo-600 dark:bg-indigo-500 h-2.5 rounded-full transition-all duration-300"
              :style="{ width: `${progressPercent}%` }"
            />
          </div>
        </div>

        <!-- Indexing Status Message (no progress info yet) -->
        <div v-if="isIndexing && !indexingTotal" class="mb-6 p-4 bg-blue-100 dark:bg-blue-900/30 border border-blue-300 dark:border-blue-700 text-blue-700 dark:text-blue-300 rounded-lg">
          <div class="flex items-center gap-2">
            <span class="inline-block animate-spin">⟳</span>
            <span>{{ progressLabel }}</span>
          </div>
        </div>

        <!-- Indexing Success -->
        <div v-if="indexingStatus === 'Indexing completed' && !isIndexing" class="mb-6 p-4 bg-green-100 dark:bg-green-900/30 border border-green-300 dark:border-green-700 text-green-700 dark:text-green-300 rounded-lg">
          <div class="flex items-center gap-2">
            <span>✓</span>
            <span>{{ indexingStatus }}</span>
            <span v-if="indexingSkipped > 0" class="text-green-500">({{ indexingSkipped }} unchanged skipped)</span>
          </div>
        </div>

        <!-- Indexing Error -->
        <div v-if="indexingError" class="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg">
          {{ indexingError }}
        </div>

        <!-- General Error -->
        <div v-if="errors.general" class="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg">
          {{ errors.general }}
        </div>

        <!-- Profile Sections -->
        <div class="space-y-6">
          <BasicInfoSection />
          <ProfessionalSummarySection />
          <LinksSection />
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
