import { ref, computed } from 'vue'
import { profileApi } from '~/api/profile'

export function useProfileIndexing() {
  const isIndexing = ref(false)
  const indexingProgress = ref(0)
  const indexingTotal = ref(0)
  const indexingStatus = ref<string | null>(null)
  const indexingError = ref<string | null>(null)
  const lastIndexedAt = ref<Date | null>(null)
  const currentTaskId = ref<string | null>(null)
  const pollingInterval = ref<ReturnType<typeof setInterval> | null>(null)

  const isLoading = computed(() => isIndexing.value)

  const progressPercent = computed(() => {
    if (indexingTotal.value === 0) return 0
    return Math.round((indexingProgress.value / indexingTotal.value) * 100)
  })

  const progressLabel = computed(() => {
    if (!isIndexing.value) return ''
    if (indexingTotal.value === 0) return 'Starting...'
    return `${indexingProgress.value} / ${indexingTotal.value} entities`
  })

  async function startIndexing(userId: string, profileId: string): Promise<void> {
    try {
      isIndexing.value = true
      indexingError.value = null
      indexingStatus.value = 'Starting indexing...'
      indexingProgress.value = 0
      indexingTotal.value = 0

      const response = await profileApi.indexProfile(userId, profileId)
      currentTaskId.value = response.task_id

      pollIndexingStatus(response.task_id)
    } catch (error: any) {
      // Handle 409 conflict (already indexing)
      if (error?.response?.status === 409) {
        indexingStatus.value = null
        isIndexing.value = false
        indexingError.value = 'Indexing already in progress for this profile'
        return
      }
      const msg = error instanceof Error ? error.message : 'Failed to start indexing'
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

        if (status.result?.current != null && status.result?.total != null) {
          indexingProgress.value = status.result.current
          indexingTotal.value = status.result.total
        }

        if (status.status === 'pending' || status.status === 'in_progress') {
          indexingStatus.value = status.status
          attempts++

          if (attempts >= maxAttempts) {
            isIndexing.value = false
            indexingError.value = 'Indexing timeout: task took too long'
            indexingStatus.value = null
            stopPolling()
          }
        } else if (status.status === 'retrying') {
          indexingStatus.value = 'Retrying...'
          attempts++
        } else if (status.status === 'completed') {
          isIndexing.value = false
          indexingStatus.value = 'Indexing completed'
          indexingProgress.value = indexingTotal.value
          lastIndexedAt.value = new Date()
          localStorage.setItem(
            `profile_indexed_at_${taskId}`,
            lastIndexedAt.value.toISOString()
          )
          stopPolling()
        } else if (status.status === 'failed') {
          isIndexing.value = false
          indexingError.value = status.error || 'Indexing failed with unknown error'
          indexingStatus.value = null
          stopPolling()
        } else if (status.status === 'cancelled') {
          isIndexing.value = false
          indexingStatus.value = 'Indexing cancelled'
          stopPolling()
        }
      } catch (error) {
        const msg = error instanceof Error ? error.message : 'Failed to get status'
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
    indexingTotal.value = 0
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
    indexingTotal,
    indexingStatus,
    indexingError,
    lastIndexedAt,
    currentTaskId,
    progressPercent,
    progressLabel,
    startIndexing,
    stopPolling,
    reset,
    loadLastIndexedTime,
  }
}
