// filepath: frontend/app/api/resume.ts
import type { ResumeImportResponse, ResumeImportStatus } from '~/types/resume'

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

export const resumeApi = {
  /**
   * Upload a PDF resume and trigger AI extraction.
   * Form fields must match backend: profile_id (string) + resume (File).
   */
  async uploadResume(profileId: string, file: File): Promise<ResumeImportResponse> {
    const formData = new FormData()
    formData.append('profile_id', profileId)
    formData.append('resume', file)   // must match backend Form field name

    return await $fetch<ResumeImportResponse>(getApiUrl('/api/v1/resume-import/upload'), {
      method: 'POST',
      body: formData,
      headers: getAuthHeaders(),
    })
  },

  /** Poll the status / extracted data of a previously uploaded resume. */
  async getResumeStatus(resumeId: string): Promise<ResumeImportStatus> {
    return await $fetch<ResumeImportStatus>(getApiUrl(`/api/v1/resume-import/status/${resumeId}`), {
      method: 'GET',
      headers: getAuthHeaders(),
    })
  },

  /** Confirm or reject a parsed resume import. */
  async confirmImport(resumeId: string, confirm: boolean): Promise<ResumeImportStatus> {
    return await $fetch<ResumeImportStatus>(getApiUrl('/api/v1/resume-import/confirm'), {
      method: 'POST',
      body: { resume_id: resumeId, confirm },
      headers: getAuthHeaders(),
    })
  },

  /** List all resumes uploaded by the current user. */
  async listResumes(): Promise<{ resumes: ResumeImportResponse[] }> {
    return await $fetch<{ resumes: ResumeImportResponse[] }>(getApiUrl('/api/v1/resume-import/list'), {
      method: 'GET',
      headers: getAuthHeaders(),
    })
  },
}
