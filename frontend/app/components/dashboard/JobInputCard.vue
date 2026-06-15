<script setup lang="ts">
import { resumeGenerationApi } from '~/api/resumeGeneration'
import { useProfileStore } from '~/stores/profileStore'

const profileStore = useProfileStore()

const jobDescription = ref<string>('')
const isProcessing = ref<boolean>(false)
const error = ref<string | null>(null)

const characterCount = computed(() => jobDescription.value.length)
const canProceed = computed(() =>
  jobDescription.value.trim().length > 50
)

const handleGenerate = async () => {
  if (!canProceed.value) return

  const profileId = profileStore.activeProfile.value?.uuid
  if (!profileId) {
    error.value = 'No active profile found'
    return
  }

  isProcessing.value = true
  error.value = null

  try {
    const result = await resumeGenerationApi.generate(profileId, {
      job_description_text: jobDescription.value.trim(),
    })
    await navigateTo(`/cv-editor?draft=${result.draft_uuid}`)
  } catch (err: any) {
    error.value = err?.message || err?.data?.message || 'Failed to generate resume'
  } finally {
    isProcessing.value = false
  }
}
</script>


<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow duration-200">
    <div class="flex items-center mb-4">
      <div class="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-full mr-4">
        <Icon name="mdi:briefcase-search" class="text-2xl text-blue-600 dark:text-blue-400" />
      </div>
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Paste Job Description
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Start by pasting the job you want to apply for
        </p>
      </div>
    </div>

    <div class="space-y-4">
      <div>
        <label for="jobDescription" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Description
        </label>
        <textarea
          id="jobDescription"
          v-model="jobDescription"
          rows="12"
          placeholder="Paste the full job description here..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
        />
        <div class="flex justify-between items-center mt-2">
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ characterCount }} characters
          </p>
        </div>
      </div>

      <div v-if="error" class="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-700 rounded-lg p-3">
        <p class="text-sm text-red-700 dark:text-red-300">{{ error }}</p>
      </div>

      <div class="flex justify-end">
        <button
          :disabled="!canProceed || isProcessing"
          class="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-medium rounded-lg transition-colors disabled:cursor-not-allowed"
          @click="handleGenerate"
        >
          <Icon v-if="isProcessing" name="mdi:loading" class="animate-spin mr-2" />
          {{ isProcessing ? 'Generating...' : 'Generate Tailored Resume' }}
        </button>
      </div>
    </div>
  </div>
</template>
