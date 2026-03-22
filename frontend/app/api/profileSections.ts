import type { 
  ProfessionalSummary, Education, WorkExperience, Project, 
  Skill, Certificate, Language, ProfileLink, CustomSection 
} from '../types/profile'

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

// Generalized API hook for hitting nested profile endpoints
function createSectionApi<T>(endpoint: string) {
  return {
    // Note: profileUuid must be the UUID string
    getAll: (profileUuid: string) => 
      $fetch<T[]>(getApiUrl(`/api/v1/profiles/${profileUuid}/${endpoint}`), {
        headers: getAuthHeaders()
      }),
      
    create: (profileUuid: string, data: Omit<T, 'uuid'>) => 
      $fetch<T>(getApiUrl(`/api/v1/profiles/${profileUuid}/${endpoint}/`), {
        method: 'POST',
        body: data,
        headers: getAuthHeaders()
      }),
      
    update: (profileUuid: string, itemUuid: string, data: Partial<Omit<T, 'uuid'>>) => 
      $fetch<T>(getApiUrl(`/api/v1/profiles/${profileUuid}/${endpoint}/${itemUuid}`), {
        method: 'PUT',
        body: data,
        headers: getAuthHeaders()
      }),
      
    delete: (profileUuid: string, itemUuid: string) => 
      $fetch<void>(getApiUrl(`/api/v1/profiles/${profileUuid}/${endpoint}/${itemUuid}`), {
        method: 'DELETE',
        headers: getAuthHeaders()
      })
  }
}

// Export pre-configured APIs for each section types
export const professionalSummaryApi = {
  ...createSectionApi<ProfessionalSummary>('professional-summaries'),
  setAsDefault: (profileUuid: string, summaryUuid: string) =>
    $fetch<ProfessionalSummary>(getApiUrl(`/api/v1/profiles/${profileUuid}/professional-summaries/${summaryUuid}/set-default`), {
      method: 'PATCH',
      headers: getAuthHeaders()
    })
}
export const educationApi = createSectionApi<Education>('education')
export const experienceApi = createSectionApi<WorkExperience>('work-experiences')
export const projectApi = createSectionApi<Project>('projects')
export const skillApi = createSectionApi<Skill>('skills')
export const certificateApi = createSectionApi<Certificate>('certificates')
export const languageApi = createSectionApi<Language>('languages')
export const profileLinkApi = createSectionApi<ProfileLink>('links')
export const customSectionApi = createSectionApi<CustomSection>('custom-sections')
