import { ref, reactive, computed } from 'vue'
import { indexingApi } from '~/api/indexing'
import type { EntityIndexingStatus, IndexingStatusResponse } from '~/api/indexing'
import { useUserStore } from '~/stores/userStore'
import { useToast } from '~/composables/useToast'

export function useIndexingStatus() {
  const { user } = useUserStore()
  const toast = useToast()

  const entityStatuses = ref<Map<string, EntityIndexingStatus>>(new Map())
  const profileIndexedAt = ref<string | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)
  const reindexingEntities = reactive<Set<string>>(new Set())

  function isReindexing(entityUuid: string): boolean {
    return reindexingEntities.has(entityUuid)
  }

  const summary = computed(() => {
    const statuses = Array.from(entityStatuses.value.values())
    return {
      total: statuses.length,
      indexed: statuses.filter(s => s.status === 'indexed').length,
      needsReindex: statuses.filter(s => s.status === 'needs_reindex').length,
      neverIndexed: statuses.filter(s => s.status === 'never_indexed').length,
    }
  })

  function getStatus(entityUuid: string): EntityIndexingStatus | undefined {
    return entityStatuses.value.get(entityUuid)
  }

  function needsReindex(entityUuid: string): boolean {
    const status = entityStatuses.value.get(entityUuid)
    return status?.needs_reindex ?? true
  }

  async function refreshStatus(profileId: string): Promise<void> {
    if (!user.value?.uuid) return
    isLoading.value = true
    error.value = null
    try {
      const response = await indexingApi.getEntityIndexingStatus(profileId, user.value.uuid)
      const map = new Map<string, EntityIndexingStatus>()
      for (const entity of response.entities) {
        map.set(entity.uuid, entity)
        if (entity.status === 'indexed' && reindexingEntities.has(entity.uuid)) {
          reindexingEntities.delete(entity.uuid)
        }
      }
      entityStatuses.value = map
      profileIndexedAt.value = response.profile_indexed_at
    } catch (err) {
      const msg = err instanceof Error ? err.message : 'Failed to fetch indexing status'
      error.value = msg
    } finally {
      isLoading.value = false
    }
  }

  async function reindexEntity(profileId: string, entityUuid: string): Promise<string | null> {
    if (!user.value?.uuid) return null
    error.value = null

    // Don't start if already indexed
    const current = entityStatuses.value.get(entityUuid)
    if (current?.status === 'indexed') {
      toast.warning('Entity is already indexed')
      return null
    }

    reindexingEntities.add(entityUuid)
    toast.info('Starting reindex...')
    try {
      const response = await indexingApi.reindexEntity(profileId, entityUuid, user.value.uuid)
      toast.info('Reindex task started')
      return response.task_id
    } catch (err: any) {
      reindexingEntities.delete(entityUuid)
      if (err?.response?.status === 409) {
        error.value = 'Indexing already in progress for this entity'
        toast.warning('Indexing already in progress for this entity')
      } else if (err?.response?.status === 400) {
        const msg = err?.response?.data?.message ?? 'Entity is already indexed'
        error.value = msg
        toast.warning(msg)
      } else {
        const msg = err instanceof Error ? err.message : 'Failed to reindex entity'
        error.value = msg
        toast.error(msg)
      }
      return null
    }
  }

  function updateEntityStatus(entityUuid: string, status: EntityIndexingStatus['status']): void {
    const current = entityStatuses.value.get(entityUuid)
    if (current) {
      entityStatuses.value.set(entityUuid, { ...current, status, needs_reindex: status !== 'indexed' })
    }
  }

  function markEntityAsIndexed(entityUuid: string): void {
    reindexingEntities.delete(entityUuid)
    const current = entityStatuses.value.get(entityUuid)
    if (current) {
      entityStatuses.value.set(entityUuid, {
        ...current,
        status: 'indexed',
        needs_reindex: false,
        indexed_at: new Date().toISOString(),
      })
      toast.success('Entity indexed successfully')
    }
  }

  function reset(): void {
    entityStatuses.value = new Map()
    profileIndexedAt.value = null
    isLoading.value = false
    error.value = null
  }

  return {
    entityStatuses,
    profileIndexedAt,
    isLoading,
    error,
    summary,
    getStatus,
    needsReindex,
    isReindexing,
    refreshStatus,
    reindexEntity,
    updateEntityStatus,
    markEntityAsIndexed,
    reset,
  }
}
