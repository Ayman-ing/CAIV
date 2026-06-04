<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { resumeDraftApi } from '~/api/resumeDraft'
import { useProfileStore } from '~/stores/profileStore'

const { activeProfile, profiles } = useProfileStore()

const drafts = ref<any[]>([])
const isLoading = ref(true)

const profileId = computed(() => activeProfile.value?.uuid || profiles.value[0]?.uuid)

onMounted(async () => {
  await loadDrafts()
})

async function loadDrafts() {
  if (!profileId.value) {
    isLoading.value = false
    return
  }
  try {
    const all = await resumeDraftApi.listDrafts(profileId.value)
    drafts.value = all.slice(0, 3)
  } catch {
    drafts.value = []
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div>
    <div v-if="isLoading" class="text-center py-8 text-gray-500 dark:text-gray-400">
      <Icon name="heroicons:arrow-path" class="w-6 h-6 mx-auto mb-2 animate-spin" />
      <p class="text-sm">Loading resumes...</p>
    </div>

    <div v-else-if="drafts.length === 0" class="text-center py-8">
      <div class="p-3 bg-gray-50 dark:bg-gray-700/50 rounded-full w-14 h-14 mx-auto mb-3 flex items-center justify-center">
        <Icon name="heroicons:document-plus" class="w-6 h-6 text-gray-400" />
      </div>
      <p class="text-sm text-gray-600 dark:text-gray-400">
        No resumes yet. Go to the CV Editor to create one.
      </p>
    </div>

    <div v-else class="space-y-3">
      <NuxtLink
        v-for="draft in drafts"
        :key="draft.uuid"
        :to="`/cv-editor?draft=${draft.uuid}`"
        class="flex items-center justify-between p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md hover:border-blue-300 dark:hover:border-blue-700 transition-all group"
      >
        <div class="flex items-center space-x-3 min-w-0">
          <div class="p-2 bg-blue-50 dark:bg-blue-900/30 rounded-lg flex-shrink-0">
            <Icon name="heroicons:document-text" class="w-5 h-5 text-blue-600 dark:text-blue-400" />
          </div>
          <div class="min-w-0">
            <h4 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
              {{ draft.title }}
            </h4>
            <p class="text-xs text-gray-500 dark:text-gray-400">
              {{ draft.template_name }} &middot; {{ formatDate(draft.updated_at) }}
            </p>
          </div>
        </div>
        <Icon name="heroicons:chevron-right" class="w-4 h-4 text-gray-400 group-hover:text-blue-500 transition-colors flex-shrink-0" />
      </NuxtLink>
    </div>
  </div>
</template>
