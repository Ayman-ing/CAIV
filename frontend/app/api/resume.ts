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

  /** Create a new generated resume for a profile with the specified template. */
  async createResume(profileId: string, template: string, title: string): Promise<any> {
    return await $fetch<any>(getApiUrl('/api/v1/resumes'), {
      method: 'POST',
      body: { profile_id: profileId, template_name: template, title },
      headers: getAuthHeaders(),
    })
  },

  /** Get a specific generated resume with all its components and data. */
  async getResume(resumeUuid: string): Promise<any> {
    return await $fetch<any>(getApiUrl(`/api/v1/resumes/${resumeUuid}`), {
      method: 'GET',
      headers: getAuthHeaders(),
    })
  },

  /** Update a generated resume. */
  async updateResume(resumeUuid: string, data: Record<string, any>): Promise<any> {
    return await $fetch<any>(getApiUrl(`/api/v1/resumes/${resumeUuid}`), {
      method: 'PUT',
      body: data,
      headers: getAuthHeaders(),
    })
  },

  /** Export resume as PDF (returns file download). */
  async exportPDF(resumeUuid: string): Promise<Blob> {
    return await $fetch<Blob>(getApiUrl(`/api/v1/resumes/${resumeUuid}/export`), {
      method: 'GET',
      headers: getAuthHeaders(),
      responseType: 'blob',
    })
  },
}
