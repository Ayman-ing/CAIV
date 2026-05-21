import { ref, computed } from 'vue'
import { profileApi } from '~/api/profile'

export function useProfileIndexing() {
  const isIndexing = ref(false)
  const indexingProgress = ref(0)
  const indexingStatus = ref<string | null>(null)
  const indexingError = ref<string | null>(null)
  const lastIndexedAt = ref<Date | null>(null)
  const currentTaskId = ref<string | null>(null)
  const pollingInterval = ref<ReturnType<typeof setInterval> | null>(null)

  const isLoading = computed(() => isIndexing.value)

  async function startIndexing(userId: string, profileId: string): Promise<void> {
    try {
      isIndexing.value = true
      indexingError.value = null
      indexingStatus.value = 'Starting indexing...'

      console.log(`[IndexProfile] Starting indexing for profile ${profileId} (user ${userId})`)
      const response = await profileApi.indexProfile(userId, profileId)
      currentTaskId.value = response.task_id
      console.log(`[IndexProfile] Task created: ${response.task_id} (status: ${response.status})`)

      pollIndexingStatus(response.task_id)
    } catch (error) {
      const msg = error instanceof Error ? error.message : 'Failed to start indexing'
      console.error(`[IndexProfile] Failed to start: ${msg}`)
      indexingError.value = msg
      indexingStatus.value = null
      isIndexing.value = false
    }
  }

  function pollIndexingStatus(taskId: string): void {
    const maxAttempts = 360
    let attempts = 0

    pollingInterval.value = setInterval(async () => {
      try {
        const status = await profileApi.getIndexingStatus(taskId)

        if (status.status === 'pending' || status.status === 'in_progress' ) {
          if (indexingStatus.value !== status.status) {
            console.log(`[IndexProfile] Status update: ${status.status}`)
          }
          indexingStatus.value = status.status
          attempts++

          if (attempts >= maxAttempts) {
            console.warn(`[IndexProfile] Timeout after ${maxAttempts} attempts`)
            isIndexing.value = false
            indexingError.value = 'Indexing timeout: task took too long'
            indexingStatus.value = null
            stopPolling()
          }
        } else if (status.status === 'retrying') {
          console.warn(`[IndexProfile] Task is retrying...`)
          indexingStatus.value = 'Retrying...'
          attempts++
        } else if (status.status === 'completed') {
          console.log(`[IndexProfile] Completed after ${attempts} poll attempts`)
          isIndexing.value = false
          indexingStatus.value = 'Indexing completed'
          lastIndexedAt.value = new Date()
          localStorage.setItem(
            `profile_indexed_at_${taskId}`,
            lastIndexedAt.value.toISOString()
          )
          stopPolling()
        } else if (status.status === 'failed') {
          console.error(`[IndexProfile] Failed: ${status.error || 'unknown error'}`)
          isIndexing.value = false
          indexingError.value = status.error || 'Indexing failed with unknown error'
          indexingStatus.value = null
          stopPolling()
        } else if (status.status === 'cancelled') {
          console.warn(`[IndexProfile] Cancelled`)
          isIndexing.value = false
          indexingStatus.value = 'Indexing cancelled'
          stopPolling()
        }
      } catch (error) {
        const msg = error instanceof Error ? error.message : 'Failed to get status'
        console.error(`[IndexProfile] Poll error: ${msg}`)
        indexingError.value = msg
        isIndexing.value = false
        stopPolling()
      }
    }, 5000)
  }

  function stopPolling(): void {
    if (pollingInterval.value !== null) {
      clearInterval(pollingInterval.value)
      pollingInterval.value = null
    }
  }

  function reset(): void {
    stopPolling()
    isIndexing.value = false
    indexingProgress.value = 0
    indexingStatus.value = null
    indexingError.value = null
    currentTaskId.value = null
  }

  function loadLastIndexedTime(): void {
    if (import.meta.client) {
      for (let i = 0; i < localStorage.length; i++) {
        const key = localStorage.key(i)
        if (key?.startsWith('profile_indexed_at_')) {
          const timestamp = localStorage.getItem(key)
          if (timestamp) {
            lastIndexedAt.value = new Date(timestamp)
          }
        }
      }
    }
  }

  return {
    isIndexing,
    isLoading,
    indexingProgress,
    indexingStatus,
    indexingError,
    lastIndexedAt,
    currentTaskId,
    startIndexing,
    stopPolling,
    reset,
    loadLastIndexedTime,
  }
}
