export interface ResumeImportResponse {
  resume_id: string
  filename: string
  status: 'pending' | 'confirmed' | 'rejected' | string
  extracted_data: {
    contact_info?: {
      name?: string
      email?: string
      phone?: string
      location?: string
    }
    education?: Array<{
      institution?: string
      degree?: string
      field_of_study?: string
      start_date?: string
      end_date?: string
      gpa?: number
      description?: string
    }>
    work_experiences?: Array<{
      job_title?: string
      company?: string
      start_date?: string
      end_date?: string
      description?: string
    }>
    skills?: Array<{
      name?: string
      category?: string
      proficiency?: string
      years_experience?: number
    }>
    languages?: Array<{
      language?: string
      proficiency?: string
      can_read?: boolean
      can_write?: boolean
      can_speak?: boolean
    }>
    projects?: Array<{
      name?: string
      description?: string
      start_date?: string
      end_date?: string
      url?: string
      technologies?: string[]
    }>
    professional_summaries?: Array<{
      title?: string
      content?: string
    }>
    certificates?: Array<{
      name?: string
      issuing_organization?: string
      issue_date?: string
      expiration_date?: string
      credential_id?: string
      credential_url?: string
    }>
    custom_sections?: Array<{
      title?: string
      content?: string
      order_index?: number
    }>
  }
  created_at: string
}

export interface ResumeImportStatus {
  resume_id: string
  status: 'pending' | 'confirmed' | 'rejected' | string
  extracted_data?: ResumeImportResponse['extracted_data']
  updated_at: string
}
