// filepath: frontend/app/services/resumeService.ts
import { resumeApi } from '~/api/resume'
import { useProfileStore } from '~/stores/profileStore'
import type { ResumeImportResponse, ResumeImportStatus } from '~/types/resume'

export const resumeService = {
  /**
   * Upload a PDF resume for the given profile and kick off AI extraction.
   * The active profile's UUID is resolved from the profile store.
   */
  async uploadResume(profileId: string, file: File): Promise<ResumeImportResponse> {
    try {
      const response = await resumeApi.uploadResume(profileId, file)
      return response
    } catch (error) {
      console.error('Error uploading resume:', error)
      throw error
    }
  },

  /** Poll status until the resume is no longer "pending", or return current state. */
  async getResumeStatus(resumeId: string): Promise<ResumeImportStatus> {
    return resumeApi.getResumeStatus(resumeId)
  },

  /** Confirm (accept) a parsed resume so it persists in the profile. */
  async confirmImport(resumeId: string): Promise<ResumeImportStatus> {
    return resumeApi.confirmImport(resumeId, true)
  },

  /** Reject a parsed resume. */
  async rejectImport(resumeId: string): Promise<ResumeImportStatus> {
    return resumeApi.confirmImport(resumeId, false)
  },
}
