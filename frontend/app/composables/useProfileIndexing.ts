import { ref, computed } from 'vue'
import { indexingApi } from '~/api/indexing'
import { useUserStore } from '~/stores/userStore'

export type EntityIndexedCallback = (entityUuid: string, section: string, status: string) => void

export function useProfileIndexing() {
  const { user } = useUserStore()

  const isIndexing = ref(false)
  const indexingProgress = ref(0)
  const indexingTotal = ref(0)
  const indexingStatus = ref<string | null>(null)
  const indexingError = ref<string | null>(null)
  const indexingPhase = ref<string | null>(null)
  const indexingSkipped = ref(0)
  const indexingSection = ref<string | null>(null)
  const lastIndexedAt = ref<Date | null>(null)
  const eventSource = ref<EventSource | null>(null)

  let persistentEventSource: EventSource | null = null
  const sseReconnectTimer = ref<ReturnType<typeof setTimeout> | null>(null)
  let reconnectAttempts = 0
  const MAX_RECONNECT_DELAY = 30000

  const isLoading = computed(() => isIndexing.value)

  const progressPercent = computed(() => {
    if (indexingTotal.value === 0) return 0
    return Math.round((indexingProgress.value / indexingTotal.value) * 100)
  })

  const progressLabel = computed(() => {
    if (!isIndexing.value) return ''
    if (indexingTotal.value === 0) {
      if (indexingPhase.value === 'collecting') return 'Collecting profile items...'
      if (indexingPhase.value === 'analyzing') return 'Checking for changes...'
      return 'Starting...'
    }
    const base = `${indexingProgress.value} / ${indexingTotal.value}`
    if (indexingPhase.value === 'embedding') return `Generating embeddings (${base})`
    if (indexingPhase.value === 'persisting') {
      if (indexingSection.value) return `Saving ${indexingSection.value} (${base})`
      return `Saving (${base})`
    }
    return `${base} entities`
  })

  let onEntityIndexedCallback: EntityIndexedCallback | null = null

  function onEntityIndexed(cb: EntityIndexedCallback): void {
    onEntityIndexedCallback = cb
  }

  async function startIndexing(userId: string, profileId: string): Promise<void> {
    try {
      isIndexing.value = true
      indexingError.value = null
      indexingStatus.value = 'Starting indexing...'
      indexingProgress.value = 0
      indexingTotal.value = 0

      const response = await indexingApi.indexProfile(userId, profileId)
      connectSSE(profileId, userId)
    } catch (error: any) {
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

  function connectSSE(profileId: string, userId: string): void {
    if (!import.meta.client || !window.EventSource) return

    const url = indexingApi.getSSEUrl(profileId, userId)

    try {
      const es = new EventSource(url)
      eventSource.value = es

      es.addEventListener('connected', () => {
        indexingStatus.value = 'Indexing started...'
      })

      es.addEventListener('progress', (event) => {
        try {
          const d = JSON.parse(event.data)
          if (d.current != null && d.total != null) {
            indexingProgress.value = d.current
            indexingTotal.value = d.total
            indexingPhase.value = d.phase || null
            indexingSkipped.value = d.skipped ?? 0
            indexingSection.value = d.section || null
          }
        } catch { /* skip malformed */ }
      })

      es.addEventListener('entity_indexed', (event) => {
        try {
          const d = JSON.parse(event.data)
          if (d.entity_uuid) {
            onEntityIndexedCallback?.(d.entity_uuid, d.section || '', d.status || 'completed')
          }
        } catch { /* skip malformed */ }
      })

      es.addEventListener('completed', () => {
        isIndexing.value = false
        indexingStatus.value = 'Indexing completed'
        indexingProgress.value = indexingTotal.value || 1
        lastIndexedAt.value = new Date()
        disconnectSSE()
      })

      es.addEventListener('error', () => {
        isIndexing.value = false
        indexingError.value = 'Indexing error occurred'
        indexingStatus.value = null
        disconnectSSE()
      })

      es.onerror = () => {
        disconnectSSE()
        isIndexing.value = false
        indexingError.value = 'SSE connection lost'
        indexingStatus.value = null
      }

    } catch {
      isIndexing.value = false
      indexingError.value = 'Failed to connect to indexing stream'
    }
  }

  function disconnectSSE(): void {
    if (eventSource.value) {
      eventSource.value.close()
      eventSource.value = null
    }
  }

  function _handleEntityIndexed(event: MessageEvent): void {
    try {
      const d = JSON.parse(event.data)
      if (d.entity_uuid) {
        onEntityIndexedCallback?.(d.entity_uuid, d.section || '', d.status || 'completed')
      }
    } catch { /* skip malformed */ }
  }

  function _getReconnectDelay(): number {
    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), MAX_RECONNECT_DELAY)
    return delay + Math.random() * 1000
  }

  function _scheduleReconnect(profileId: string, userId: string): void {
    if (persistentEventSource) return
    if (sseReconnectTimer.value) return

    const delay = _getReconnectDelay()
    reconnectAttempts++
    sseReconnectTimer.value = setTimeout(() => {
      sseReconnectTimer.value = null
      connectPersistentSSE(profileId, userId)
    }, delay)
  }

  function connectPersistentSSE(profileId: string, userId: string): void {
    if (persistentEventSource) return

    const url = indexingApi.getSSEUrl(profileId, userId)
    try {
      const es = new EventSource(url)
      persistentEventSource = es

      es.addEventListener('entity_indexed', _handleEntityIndexed)

      es.addEventListener('completed', () => {
        persistentEventSource = null
        es.close()
      })

      es.addEventListener('error', () => {
        persistentEventSource = null
        es.close()
        _scheduleReconnect(profileId, userId)
      })

      es.onerror = () => {
        persistentEventSource = null
        es.close()
        _scheduleReconnect(profileId, userId)
      }

      reconnectAttempts = 0
    } catch {
      _scheduleReconnect(profileId, userId)
    }
  }

  function disconnectPersistentSSE(): void {
    if (persistentEventSource) {
      persistentEventSource.close()
      persistentEventSource = null
    }
    if (sseReconnectTimer.value) {
      clearTimeout(sseReconnectTimer.value)
      sseReconnectTimer.value = null
    }
    reconnectAttempts = 0
  }

  function reset(): void {
    disconnectSSE()
    disconnectPersistentSSE()
    isIndexing.value = false
    indexingProgress.value = 0
    indexingTotal.value = 0
    indexingStatus.value = null
    indexingError.value = null
    indexingPhase.value = null
    indexingSkipped.value = 0
    indexingSection.value = null
    lastIndexedAt.value = null
    onEntityIndexedCallback = null
  }

  return {
    isIndexing,
    isLoading,
    indexingProgress,
    indexingTotal,
    indexingStatus,
    indexingError,
    indexingPhase,
    indexingSkipped,
    indexingSection,
    lastIndexedAt,
    progressPercent,
    progressLabel,
    startIndexing,
    reset,
    onEntityIndexed,
    disconnectSSE,
    connectPersistentSSE,
    disconnectPersistentSSE,
  }
}
