<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { resumeDraftApi } from '~/api/resumeDraft'
import { useProfileStore } from '~/stores/profileStore'
import { useToast } from '~/composables/useToast'

const { activeProfile, profiles } = useProfileStore()
const { success, error } = useToast()

const drafts = ref<any[]>([])
const isLoading = ref(true)
const confirmDelete = ref<string | null>(null)

const profileId = computed(() => activeProfile.value?.uuid || profiles.value[0]?.uuid)

onMounted(async () => {
  await loadDrafts()
})

async function loadDrafts() {
  if (!profileId.value) {
    isLoading.value = false
    return
  }
  isLoading.value = true
  try {
    drafts.value = await resumeDraftApi.listDrafts(profileId.value)
  } catch {
    error('Failed to load resumes', 3000)
  } finally {
    isLoading.value = false
  }
}

async function handleDelete(uuid: string) {
  try {
    await resumeDraftApi.deleteDraft(profileId.value!, uuid)
    drafts.value = drafts.value.filter(d => d.uuid !== uuid)
    confirmDelete.value = null
    success('Resume deleted', 2000)
  } catch {
    error('Failed to delete resume', 3000)
  }
}

const formatDate = (dateStr: string) => {
  const d = new Date(dateStr)
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })
}
</script>

<template>
  <div class="py-8 px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 max-w-none">
    <div class="flex items-center justify-between mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-gray-100">My Resumes</h1>
        <p class="text-sm text-gray-600 dark:text-gray-400 mt-1">
          Manage all your created resume drafts
        </p>
      </div>
      <NuxtLink
        to="/cv-editor"
        class="inline-flex items-center space-x-2 px-4 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Icon name="heroicons:plus" class="w-4 h-4" />
        <span>Create New Resume</span>
      </NuxtLink>
    </div>

    <div v-if="isLoading" class="text-center py-16 text-gray-500 dark:text-gray-400">
      <Icon name="heroicons:arrow-path" class="w-8 h-8 mx-auto mb-2 animate-spin" />
      <p>Loading resumes...</p>
    </div>

    <div v-else-if="drafts.length === 0" class="text-center py-16 bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700">
      <Icon name="heroicons:document-text" class="w-12 h-12 mx-auto mb-3 text-gray-300 dark:text-gray-600" />
      <h2 class="text-lg font-medium text-gray-900 dark:text-gray-100 mb-2">No resumes yet</h2>
      <p class="text-sm text-gray-500 dark:text-gray-400 mb-6">
        Create your first resume draft to get started
      </p>
      <NuxtLink
        to="/cv-editor"
        class="inline-flex items-center px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors"
      >
        <Icon name="heroicons:plus" class="w-4 h-4 mr-1" />
        Create Your First Resume
      </NuxtLink>
    </div>

    <div v-else class="bg-white dark:bg-gray-800 rounded-lg border border-gray-200 dark:border-gray-700 overflow-hidden">
      <div class="divide-y divide-gray-200 dark:divide-gray-700">
        <div
          v-for="draft in drafts"
          :key="draft.uuid"
          class="flex items-center justify-between px-6 py-4 hover:bg-gray-50 dark:hover:bg-gray-700/50 transition-colors group"
        >
          <NuxtLink
            :to="`/cv-editor?draft=${draft.uuid}`"
            class="flex-1 min-w-0"
          >
            <h3 class="text-sm font-medium text-gray-900 dark:text-gray-100 truncate">
              {{ draft.title }}
            </h3>
            <div class="flex items-center space-x-3 mt-1">
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ draft.template_name }}
              </span>
              <span class="text-xs text-gray-400">&middot;</span>
              <span class="text-xs text-gray-500 dark:text-gray-400">
                Updated {{ formatDate(draft.updated_at) }}
              </span>
            </div>
          </NuxtLink>
          <div class="flex items-center space-x-2 flex-shrink-0 ml-4">
            <NuxtLink
              :to="`/cv-editor?draft=${draft.uuid}`"
              class="p-1.5 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Edit"
            >
              <Icon name="heroicons:pencil-square" class="w-4 h-4" />
            </NuxtLink>
            <button
              v-if="confirmDelete !== draft.uuid"
              class="p-1.5 text-gray-400 hover:text-red-600 dark:hover:text-red-400 opacity-0 group-hover:opacity-100 transition-opacity"
              title="Delete"
              @click="confirmDelete = draft.uuid"
            >
              <Icon name="heroicons:trash" class="w-4 h-4" />
            </button>
            <div v-else class="flex items-center space-x-1">
              <button
                class="text-xs text-red-600 dark:text-red-400 hover:underline"
                @click="handleDelete(draft.uuid)"
              >
                Delete
              </button>
              <button
                class="text-xs text-gray-400 hover:underline"
                @click="confirmDelete = null"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
