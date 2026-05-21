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

  /**
   * Create a new generated resume for a profile.
   */
  async createResume(profileId: string, template: string = 'MODERN', title: string = 'My Resume'): Promise<any> {
    try {
      const response = await resumeApi.createResume(profileId, template, title)
      return response
    } catch (error) {
      console.error('Error creating resume:', error)
      throw error
    }
  },

  /**
   * Get a specific generated resume with all its components and data.
   */
  async getResume(resumeUuid: string): Promise<any> {
    try {
      const response = await resumeApi.getResume(resumeUuid)
      return response
    } catch (error) {
      console.error('Error fetching resume:', error)
      throw error
    }
  },

  /**
   * Update a generated resume.
   */
  async updateResume(resumeUuid: string, data: Record<string, any>): Promise<any> {
    try {
      const response = await resumeApi.updateResume(resumeUuid, data)
      return response
    } catch (error) {
      console.error('Error updating resume:', error)
      throw error
    }
  },

  /**
   * Download resume as PDF.
   */
  async downloadPDF(resumeUuid: string, filename: string = 'resume.pdf'): Promise<void> {
    try {
      const blob = await resumeApi.exportPDF(resumeUuid)
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      link.download = filename
      document.body.appendChild(link)
      link.click()
      window.URL.revokeObjectURL(url)
      document.body.removeChild(link)
    } catch (error) {
      console.error('Error downloading PDF:', error)
      throw error
    }
  },

  /**
   * Get PDF as data URL for preview (for PDF viewer component).
   */
  async getPDFPreview(resumeUuid: string): Promise<string> {
    try {
      const blob = await resumeApi.exportPDF(resumeUuid)
      return URL.createObjectURL(blob)
    } catch (error) {
      console.error('Error getting PDF preview:', error)
      throw error
    }
  },
}
