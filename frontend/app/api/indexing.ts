import type { Profile } from '~/types/profile'

export interface IndexingResponse {
  task_id: string
  message: string
  profile_uuid: string
  status: string
}

export interface EntityIndexingStatus {
  uuid: string
  entity_type: string
  updated_at: string
  indexed_at: string | null
  needs_reindex: boolean
  status: 'indexed' | 'needs_reindex' | 'never_indexed'
}

export interface IndexingStatusResponse {
  profile_uuid: string
  entities: EntityIndexingStatus[]
  profile_indexed_at: string | null
  total_entities: number
  indexed_count: number
  needs_reindex_count: number
  never_indexed_count: number
}

export interface EntityIndexingResponse {
  task_id: string
  entity_uuid: string
  status: string
}

const getApiUrl = (endpoint: string) => {
  const config = useRuntimeConfig()
  return `${config.public.apiBase}${endpoint}`
}

const getAuthHeaders = (): Record<string, string> => {
  if (process.client) {
    const token = localStorage.getItem('access_token')
    if (token) return { 'Authorization': `Bearer ${token}` }
  }
  return {}
}

export const indexingApi = {
  async indexProfile(userId: string, profileId: string): Promise<IndexingResponse> {
    return await $fetch<IndexingResponse>(getApiUrl(`/api/v1/profiles/${profileId}/index`), {
      method: 'POST',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  },

  async getEntityIndexingStatus(profileId: string, userId: string): Promise<IndexingStatusResponse> {
    return await $fetch<IndexingStatusResponse>(getApiUrl(`/api/v1/profiles/${profileId}/indexing-status`), {
      method: 'GET',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  },

  async reindexEntity(profileId: string, entityUuid: string, userId: string): Promise<EntityIndexingResponse> {
    return await $fetch<EntityIndexingResponse>(getApiUrl(`/api/v1/profiles/${profileId}/entities/${entityUuid}/index`), {
      method: 'POST',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  },

  getSSEUrl(profileId: string, userId: string): string {
    const config = useRuntimeConfig()
    const token = process.client ? localStorage.getItem('access_token') : ''
    const base = `${config.public.apiBase}/api/v1/profiles/${profileId}/index/events`
    return `${base}?user_uuid=${userId}&token=${encodeURIComponent(token || '')}`
  }
}
