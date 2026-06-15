export interface GenerateRequest {
  job_description_text: string
}

export interface GenerateResponse {
  draft_uuid: string
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

export const resumeGenerationApi = {
  async generate(profileUuid: string, data: GenerateRequest): Promise<GenerateResponse> {
    return await $fetch<GenerateResponse>(
      getApiUrl(`/api/v1/profiles/${profileUuid}/generate-resume/`),
      {
        method: 'POST',
        body: data,
        headers: getAuthHeaders(),
      }
    )
  },
}
