import { computed, reactive } from 'vue'
import { resumeService } from '~/services/resumeService'
import { resumeDraftService } from '~/services/resumeDraftService'
import { useToast } from '~/composables/useToast'
import { useProfileStore } from '~/stores/profileStore'
import type { WorkExperience, Education, Skill, Project, Certificate, Language, ProfileLink, CustomSection } from '~/types/profile'

export interface ResumeComponent {
  uuid: string
  component_type: string
  component_id: number
  is_included: boolean
  order_index: number
}

export interface GeneratedResume {
  uuid: string
  template_name: string
  title: string
  components: ResumeComponent[]
  [key: string]: unknown
}

export interface ProfileData {
  basicInfo: {
    name: string
    email: string
    phone: string
    location: string
  }
  summary: string
  workExperiences: WorkExperience[]
  education: Education[]
  skills: Skill[]
  projects: Project[]
  certificates: Certificate[]
  languages: Language[]
  customSections: CustomSection[]
  links: ProfileLink[]
  skillUseCategories: boolean
}

export interface CVEditorState {
  currentResume: GeneratedResume | null
  selectedTemplate: string
  components: ResumeComponent[]
  profileData: ProfileData
  draftUuid: string | null
  draftTitle: string | null
  isLoading: boolean
  isSaving: boolean
  error: string | null
  sidebarWidths: {
    left: number
    right: number
  }
  layout: {
    fontSize: number
    lineHeight: number
    sectionSpacing: number
    pageMargins: {
      top: number
      bottom: number
      left: number
      right: number
    }
  }
}

const emptyProfileData = (): ProfileData => ({
  basicInfo: { name: '', email: '', phone: '', location: '' },
  summary: '',
  workExperiences: [],
  education: [],
  skills: [],
  projects: [],
  certificates: [],
  languages: [],
  customSections: [],
  links: [],
  skillUseCategories: false,
})

const allSectionTypes = [
  'professional_summary', 'work_experience', 'education', 'skills',
  'projects', 'certificates', 'languages', 'custom_sections',
]

function populateComponents(): ResumeComponent[] {
  return allSectionTypes.map((type, i) => ({
    uuid: crypto.randomUUID() as string,
    component_type: type,
    component_id: 0,
    is_included: true,
    order_index: i,
  }))
}

const state = reactive<CVEditorState>({
  currentResume: null,
  selectedTemplate: 'CANADIAN',
  components: populateComponents(),
  profileData: emptyProfileData(),
  draftUuid: null,
  draftTitle: null,
  isLoading: false,
  isSaving: false,
  error: null,
  sidebarWidths: {
    left: 320,
    right: 320,
  },
  layout: {
    fontSize: 11,
    lineHeight: 1.4,
    sectionSpacing: 16,
    pageMargins: { top: 40, bottom: 40, left: 40, right: 40 },
  },
})

export function useCVEditor() {
  const { error: toastError } = useToast()

  const hasChanges = computed(() => {
    if (!state.currentResume) return false
    return true
  })

  const hasResume = computed(() => !!state.currentResume)

  const includedComponents = computed(() =>
    [...state.components].sort((a, b) => a.order_index - b.order_index)
  )

  async function loadResume(resumeUuid: string): Promise<void> {
    state.isLoading = true
    state.error = null
    try {
      const resume = await resumeService.getResume(resumeUuid)
      state.currentResume = resume
      state.components = resume.components || []
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load resume'
      state.error = message
      toastError(message, 5000)
    } finally {
      state.isLoading = false
    }
  }

  function initEmptyEditor(): void {
    state.currentResume = null
    state.selectedTemplate = 'CANADIAN'
    state.components = populateComponents()
    state.profileData = emptyProfileData()
    state.draftUuid = null
    state.draftTitle = null
    state.isLoading = false
    state.error = null
    state.isSaving = false
  }

  async function createNewResume(
    profileId: string,
    title: string = 'My Resume'
  ): Promise<GeneratedResume> {
    state.isSaving = true
    state.error = null
    try {
      const resume = await resumeService.createResume(profileId, 'CANADIAN', title)
      state.currentResume = resume
      state.components = resume.components || []
      return resume
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to create resume'
      state.error = message
      toastError(message, 5000)
      throw err
    } finally {
      state.isSaving = false
    }
  }

  function addCustomSection(data: { title: string; content: string }): void {
    state.profileData.customSections.push({
      uuid: crypto.randomUUID() as string,
      title: data.title,
      content: data.content,
    })
  }

  function removeCustomSection(uuid: string): void {
    const idx = state.profileData.customSections.findIndex(s => s.uuid === uuid)
    if (idx !== -1) state.profileData.customSections.splice(idx, 1)
  }

  function reorderComponents(newOrder: ResumeComponent[]): void {
    newOrder.forEach((component, index) => {
      component.order_index = index
    })
    state.components = newOrder
  }

  function updateProfileData(data: Partial<ProfileData>): void {
    Object.assign(state.profileData, data)
  }

  function updateBasicInfo(field: keyof ProfileData['basicInfo'], value: string): void {
    state.profileData.basicInfo[field] = value
  }

  function updateSummary(content: string): void {
    state.profileData.summary = content
  }

  function ensureComponentType(type: string): void {
    if (!state.components.some(c => c.component_type === type)) {
      state.components.push({
        uuid: crypto.randomUUID(),
        component_type: type,
        component_id: 0,
        is_included: true,
        order_index: state.components.length,
      })
    }
  }

  function addWorkExperience(data: { job_title: string; company?: string; start_date?: string; end_date?: string; description?: string }): void {
    ensureComponentType('work_experience')
    state.profileData.workExperiences.push({
      uuid: crypto.randomUUID(),
      job_title: data.job_title,
      company: data.company || '',
      start_date: data.start_date || '',
      end_date: data.end_date || null,
      description: data.description || null,
    })
  }

  function removeWorkExperience(uuid: string): void {
    const idx = state.profileData.workExperiences.findIndex(e => e.uuid === uuid)
    if (idx !== -1) state.profileData.workExperiences.splice(idx, 1)
  }

  function addEducation(data: { institution: string; degree: string; field_of_study?: string; start_date?: string; end_date?: string; description?: string }): void {
    ensureComponentType('education')
    state.profileData.education.push({
      uuid: crypto.randomUUID() as string,
      institution: data.institution,
      degree: data.degree,
      field_of_study: data.field_of_study || null,
      start_date: data.start_date || '',
      end_date: data.end_date || null,
      description: data.description || null,
      gpa: null,
    } as Education)
  }

  function removeEducation(uuid: string): void {
    const idx = state.profileData.education.findIndex(e => e.uuid === uuid)
    if (idx !== -1) state.profileData.education.splice(idx, 1)
  }

  function addSkill(data: { name: string; category?: string; proficiency?: string }): void {
    ensureComponentType('skills')
    state.profileData.skills.push({
      uuid: crypto.randomUUID(),
      name: data.name,
      category: data.category || null,
      proficiency: data.proficiency || null,
    })
  }

  function removeSkill(uuid: string): void {
    const idx = state.profileData.skills.findIndex(s => s.uuid === uuid)
    if (idx !== -1) state.profileData.skills.splice(idx, 1)
  }

  function addProject(data: { name: string; description?: string; technologies?: string; start_date?: string; end_date?: string }): void {
    ensureComponentType('projects')
    state.profileData.projects.push({
      uuid: crypto.randomUUID(),
      name: data.name,
      description: data.description || null,
      technologies: data.technologies || null,
      start_date: data.start_date || '',
      end_date: data.end_date || null,
      url: null,
    })
  }

  function removeProject(uuid: string): void {
    const idx = state.profileData.projects.findIndex(p => p.uuid === uuid)
    if (idx !== -1) state.profileData.projects.splice(idx, 1)
  }

  function addCertificate(data: { name: string; issuing_organization: string; issue_date?: string }): void {
    ensureComponentType('certificates')
    state.profileData.certificates.push({
      uuid: crypto.randomUUID(),
      name: data.name,
      issuing_organization: data.issuing_organization,
      issue_date: data.issue_date || '',
      expiration_date: null,
      credential_id: null,
    })
  }

  function removeCertificate(uuid: string): void {
    const idx = state.profileData.certificates.findIndex(c => c.uuid === uuid)
    if (idx !== -1) state.profileData.certificates.splice(idx, 1)
  }

  function addLanguage(data: { language: string; proficiency: string }): void {
    ensureComponentType('languages')
    state.profileData.languages.push({
      uuid: crypto.randomUUID(),
      language: data.language,
      proficiency: data.proficiency,
    })
  }

  function removeLanguage(uuid: string): void {
    const idx = state.profileData.languages.findIndex(l => l.uuid === uuid)
    if (idx !== -1) state.profileData.languages.splice(idx, 1)
  }

  function addLink(link: ProfileLink): void {
    state.profileData.links.push(link)
  }

  function removeLink(uuid: string): void {
    const idx = state.profileData.links.findIndex(l => l.uuid === uuid)
    if (idx !== -1) state.profileData.links.splice(idx, 1)
  }

  function updateLink(uuid: string, data: Partial<ProfileLink>): void {
    const link = state.profileData.links.find(l => l.uuid === uuid)
    if (link) Object.assign(link, data)
  }

  async function saveCurrentDraft(title?: string): Promise<void> {
    const profileStore = useProfileStore()
    const profileId = profileStore.activeProfile.value?.uuid
    if (!profileId) {
      toastError('No active profile', 3000)
      return
    }
    state.isSaving = true
    try {
      const draftTitle = title || state.draftTitle || 'Untitled Draft'
      const result = await resumeDraftService.saveDraft(
        profileId,
        state.draftUuid,
        draftTitle,
        {
          components: state.components,
          profileData: state.profileData,
          selectedTemplate: state.selectedTemplate,
        }
      )
      state.draftUuid = result.uuid
      state.draftTitle = result.title
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to save draft'
      toastError(message, 5000)
      throw err
    } finally {
      state.isSaving = false
    }
  }

  async function loadDraft(draftUuid: string): Promise<void> {
    const profileStore = useProfileStore()
    const profileId = profileStore.activeProfile.value?.uuid
    if (!profileId) {
      toastError('No active profile', 3000)
      return
    }
    state.isLoading = true
    try {
      const data = await resumeDraftService.loadDraft(profileId, draftUuid)
      state.components = data.components.length > 0
        ? data.components
        : populateComponents()
      state.profileData = { ...emptyProfileData(), ...data.profileData }
      state.selectedTemplate = data.selectedTemplate
      state.draftUuid = draftUuid
      state.draftTitle = data.title
      state.currentResume = null
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to load draft'
      toastError(message, 5000)
      throw err
    } finally {
      state.isLoading = false
    }
  }

  async function listDrafts(): Promise<any[]> {
    const profileStore = useProfileStore()
    const profileId = profileStore.activeProfile.value?.uuid
    if (!profileId) return []
    try {
      return await resumeDraftService.listDrafts(profileId)
    } catch {
      return []
    }
  }

  async function deleteDraft(draftUuid: string): Promise<void> {
    const profileStore = useProfileStore()
    const profileId = profileStore.activeProfile.value?.uuid
    if (!profileId) return
    try {
      await resumeDraftService.deleteDraft(profileId, draftUuid)
      if (state.draftUuid === draftUuid) {
        state.draftUuid = null
        state.draftTitle = null
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to delete draft'
      toastError(message, 5000)
    }
  }

  async function exportPDF(): Promise<void> {
    if (!state.currentResume) return
    try {
      const filename = `${state.currentResume.title || 'resume'}.pdf`
      await resumeService.downloadPDF(state.currentResume.uuid, filename)
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to export PDF'
      state.error = message
      toastError(message, 5000)
    }
  }

  async function saveResume(): Promise<void> {
    state.isSaving = true
    try {
      if (!state.currentResume) {
        const profileStore = useProfileStore()
        const profileId = profileStore.activeProfile.value?.uuid
        if (!profileId) {
          throw new Error('No profile available. Please create a profile first.')
        }
        const resume = await resumeService.createResume(
          profileId,
          'CANADIAN',
          'My Resume'
        )
        state.currentResume = resume
        state.components = resume.components || []
      } else {
        const updated = await resumeService.updateResume(state.currentResume.uuid, {})
        state.currentResume = updated
      }
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to save resume'
      state.error = message
      toastError(message, 5000)
    } finally {
      state.isSaving = false
    }
  }

  function updateSidebarWidth(side: 'left' | 'right', width: number): void {
    const minWidth = 200
    const maxWidth = 600
    state.sidebarWidths[side] = Math.max(minWidth, Math.min(maxWidth, width))
  }

  function updateLayout<K extends keyof CVEditorState['layout']>(
    key: K,
    value: CVEditorState['layout'][K]
  ): void {
    if (key === 'pageMargins' && typeof value === 'object') {
      Object.assign(state.layout.pageMargins, value)
    } else {
      (state.layout as any)[key] = value
    }
  }

  function updatePageMargin(side: keyof typeof state.layout.pageMargins, value: number): void {
    state.layout.pageMargins[side] = Math.max(10, Math.min(80, value))
  }

  function resetState(): void {
    state.currentResume = null
    state.selectedTemplate = 'CANADIAN'
    state.components = populateComponents()
    state.profileData = emptyProfileData()
    state.draftUuid = null
    state.draftTitle = null
    state.isLoading = false
    state.isSaving = false
    state.error = null
  }

  return {
    state,
    hasChanges,
    hasResume,
    includedComponents,
    loadResume,
    initEmptyEditor,
    createNewResume,
    reorderComponents,
    updateProfileData,
    updateBasicInfo,
    updateSummary,
    addWorkExperience,
    removeWorkExperience,
    addEducation,
    removeEducation,
    addSkill,
    removeSkill,
    addProject,
    removeProject,
    addCertificate,
    removeCertificate,
    addLanguage,
    removeLanguage,
    addLink,
    removeLink,
    updateLink,
    addCustomSection,
    removeCustomSection,
    saveCurrentDraft,
    loadDraft,
    listDrafts,
    deleteDraft,
    exportPDF,
    saveResume,
    updateSidebarWidth,
    updateLayout,
    updatePageMargin,
    resetState,
  }
}
