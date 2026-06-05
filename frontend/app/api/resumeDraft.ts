export interface ResumeDraftResponse {
  uuid: string
  profile_id: number
  title: string
  template_name: string
  draft_data: Record<string, any>
  created_at: string
  updated_at: string
}

const getApiUrl = (endpoint: string) => {
  const config = useRuntimeConfig()
  return `${config.public.apiBase}${endpoint}`
}

const getAuthHeaders = (): Record<string, string> => {
  if (process.client) {
    const token = localStorage.getItem('access_token')
    if (token) return { Authorization: `Bearer ${token}` }
  }
  return {}
}

export const resumeDraftApi = {
  async createDraft(profileId: string, title: string, templateName: string, draftData: Record<string, any>): Promise<ResumeDraftResponse> {
    return await $fetch<ResumeDraftResponse>(
      getApiUrl(`/api/v1/profiles/${profileId}/resume-drafts/`),
      {
        method: 'POST',
        body: { title, template_name: templateName, draft_data: draftData },
        headers: getAuthHeaders(),
      }
    )
  },

  async getDraft(profileId: string, draftUuid: string): Promise<ResumeDraftResponse> {
    return await $fetch<ResumeDraftResponse>(
      getApiUrl(`/api/v1/profiles/${profileId}/resume-drafts/${draftUuid}`),
      { headers: getAuthHeaders() }
    )
  },

  async listDrafts(profileId: string): Promise<ResumeDraftResponse[]> {
    return await $fetch<ResumeDraftResponse[]>(
      getApiUrl(`/api/v1/profiles/${profileId}/resume-drafts/`),
      { headers: getAuthHeaders() }
    )
  },

  async updateDraft(profileId: string, draftUuid: string, data: Partial<{ title: string; template_name: string; draft_data: Record<string, any> }>): Promise<ResumeDraftResponse> {
    return await $fetch<ResumeDraftResponse>(
      getApiUrl(`/api/v1/profiles/${profileId}/resume-drafts/${draftUuid}`),
      {
        method: 'PUT',
        body: data,
        headers: getAuthHeaders(),
      }
    )
  },

  async deleteDraft(profileId: string, draftUuid: string): Promise<void> {
    await $fetch(
      getApiUrl(`/api/v1/profiles/${profileId}/resume-drafts/${draftUuid}`),
      {
        method: 'DELETE',
        headers: getAuthHeaders(),
      }
    )
  },
}
