import { 
  professionalSummaryApi, 
  educationApi, 
  experienceApi, 
  projectApi, 
  skillApi, 
  certificateApi, 
  languageApi, 
  profileLinkApi, 
  customSectionApi 
} from '~/api/profileSections'
import type { 
  ProfessionalSummary, Education, WorkExperience, Project, 
  Skill, Certificate, Language, ProfileLink, CustomSection 
} from '~/types/profile'

const createServiceLayer = <T>(api: any, name: string) => ({
  getAll: async (profileUuid: string): Promise<T[]> => {
    try {
      return await api.getAll(profileUuid)
    } catch (error) {
      console.error(`Failed to fetch ${name}`, error)
      return []
    }
  },
  create: async (profileUuid: string, data: Omit<T, 'uuid'>): Promise<T | null> => {
    try {
      return await api.create(profileUuid, data)
    } catch (error) {
      console.error(`Failed to create ${name}`, error)
      return null
    }
  },
  update: async (profileUuid: string, itemUuid: string, data: Partial<Omit<T, 'uuid'>>): Promise<T | null> => {
    try {
      return await api.update(profileUuid, itemUuid, data)
    } catch (error) {
      console.error(`Failed to update ${name}`, error)
      return null
    }
  },
  delete: async (profileUuid: string, itemUuid: string): Promise<boolean> => {
    try {
      await api.delete(profileUuid, itemUuid)
      return true
    } catch (error) {
      console.error(`Failed to delete ${name}`, error)
      return false
    }
  }
})

export const profileSectionsService = {
  // --- Professional Summaries ---
  getAllProfessionalSummaries: (profileUuid: string) => professionalSummaryApi.getAll(profileUuid),
  fetchProfessionalSummaries: (profileUuid: string) => professionalSummaryApi.getAll(profileUuid), // keeping for compat
  createProfessionalSummary: (profileUuid: string, data: any) => professionalSummaryApi.create(profileUuid, data),
  updateProfessionalSummary: (profileUuid: string, uuid: string, data: any) => professionalSummaryApi.update(profileUuid, uuid, data),
  deleteProfessionalSummary: (profileUuid: string, uuid: string) => professionalSummaryApi.delete(profileUuid, uuid),
  setDefaultProfessionalSummary: (profileUuid: string, summaryUuid: string) => professionalSummaryApi.setAsDefault(profileUuid, summaryUuid),

  // --- Education ---
  getAllEducations: (profileUuid: string) => educationApi.getAll(profileUuid),
  createEducation: (profileUuid: string, data: any) => educationApi.create(profileUuid, data),
  updateEducation: (profileUuid: string, uuid: string, data: any) => educationApi.update(profileUuid, uuid, data),
  deleteEducation: (profileUuid: string, uuid: string) => educationApi.delete(profileUuid, uuid),

  // --- Work Experience ---
  getAllWorkExperiences: (profileUuid: string) => experienceApi.getAll(profileUuid),
  createWorkExperience: (profileUuid: string, data: any) => experienceApi.create(profileUuid, data),
  updateWorkExperience: (profileUuid: string, uuid: string, data: any) => experienceApi.update(profileUuid, uuid, data),
  deleteWorkExperience: (profileUuid: string, uuid: string) => experienceApi.delete(profileUuid, uuid),

  // --- Skills ---
  getAllSkills: (profileUuid: string) => skillApi.getAll(profileUuid),
  createSkill: (profileUuid: string, data: any) => skillApi.create(profileUuid, data),
  updateSkill: (profileUuid: string, uuid: string, data: any) => skillApi.update(profileUuid, uuid, data),
  deleteSkill: (profileUuid: string, uuid: string) => skillApi.delete(profileUuid, uuid),

  // --- Projects ---
  getAllProjects: (profileUuid: string) => projectApi.getAll(profileUuid),
  createProject: (profileUuid: string, data: any) => projectApi.create(profileUuid, data),
  updateProject: (profileUuid: string, uuid: string, data: any) => projectApi.update(profileUuid, uuid, data),
  deleteProject: (profileUuid: string, uuid: string) => projectApi.delete(profileUuid, uuid),

  // --- Certificates ---
  getAllCertifications: (profileUuid: string) => certificateApi.getAll(profileUuid),
  createCertificate: (profileUuid: string, data: any) => certificateApi.create(profileUuid, data),
  updateCertificate: (profileUuid: string, uuid: string, data: any) => certificateApi.update(profileUuid, uuid, data),
  deleteCertificate: (profileUuid: string, uuid: string) => certificateApi.delete(profileUuid, uuid),

  // --- Languages ---
  getAllLanguages: (profileUuid: string) => languageApi.getAll(profileUuid),
  createLanguage: (profileUuid: string, data: any) => languageApi.create(profileUuid, data),
  updateLanguage: (profileUuid: string, uuid: string, data: any) => languageApi.update(profileUuid, uuid, data),
  deleteLanguage: (profileUuid: string, uuid: string) => languageApi.delete(profileUuid, uuid),

  // --- Profile Links ---
  getAllProfileLinks: (profileUuid: string) => profileLinkApi.getAll(profileUuid),
  createProfileLink: (profileUuid: string, data: any) => profileLinkApi.create(profileUuid, data),
  updateProfileLink: (profileUuid: string, uuid: string, data: any) => profileLinkApi.update(profileUuid, uuid, data),
  deleteProfileLink: (profileUuid: string, uuid: string) => profileLinkApi.delete(profileUuid, uuid),

  // --- Custom Sections ---
  getAllCustomSections: (profileUuid: string) => customSectionApi.getAll(profileUuid),
  createCustomSection: (profileUuid: string, data: any) => customSectionApi.create(profileUuid, data),
  updateCustomSection: (profileUuid: string, uuid: string, data: any) => customSectionApi.update(profileUuid, uuid, data),
  deleteCustomSection: (profileUuid: string, uuid: string) => customSectionApi.delete(profileUuid, uuid),
}
