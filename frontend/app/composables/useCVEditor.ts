import { computed, reactive } from 'vue'
import { resumeService } from '~/services/resumeService'
import { useToast } from '~/composables/useToast'
import { useProfileStore } from '~/stores/profileStore'

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

export interface CVEditorState {
  currentResume: GeneratedResume | null
  selectedTemplate: string
  components: ResumeComponent[]
  isLoading: boolean
  isSaving: boolean
  isGenerating: boolean
  previewUrl: string | null
  error: string | null
  sidebarWidths: {
    left: number
    right: number
  }
}

export function useCVEditor() {
  const { error: toastError } = useToast()

  const state = reactive<CVEditorState>({
    currentResume: null,
    selectedTemplate: 'MODERN',
    components: [],
    isLoading: false,
    isSaving: false,
    isGenerating: false,
    previewUrl: null,
    error: null,
    sidebarWidths: {
      left: 320,
      right: 320,
    },
  })

  const hasChanges = computed(() => {
    if (!state.currentResume) return false
    return true
  })

  const hasResume = computed(() => !!state.currentResume)

  const availableTemplates = computed(() => [
    { label: 'Modern', value: 'MODERN' },
    { label: 'Classic', value: 'CLASSIC' },
    { label: 'Creative', value: 'CREATIVE' },
    { label: 'Minimal', value: 'MINIMAL' },
    { label: 'Professional', value: 'PROFESSIONAL' },
  ])

  const includedComponents = computed(() =>
    state.components.filter(c => c.is_included).sort((a, b) => a.order_index - b.order_index)
  )

  const excludedComponents = computed(() =>
    state.components.filter(c => !c.is_included)
  )

  async function loadResume(resumeUuid: string): Promise<void> {
    state.isLoading = true
    state.error = null
    try {
      const resume = await resumeService.getResume(resumeUuid)
      state.currentResume = resume
      state.selectedTemplate = resume.template_name || 'MODERN'
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
    state.selectedTemplate = 'MODERN'
    state.components = []
    state.isLoading = false
    state.error = null
    state.isSaving = false
    state.isGenerating = false
    state.previewUrl = null
  }

  async function createNewResume(
    profileId: string,
    template: string = 'MODERN',
    title: string = 'My Resume'
  ): Promise<GeneratedResume> {
    state.isSaving = true
    state.error = null
    try {
      const resume = await resumeService.createResume(profileId, template, title)
      state.currentResume = resume
      state.selectedTemplate = resume.template_name || template
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

  function updateTemplate(template: string): void {
    state.selectedTemplate = template
  }

  function toggleComponent(componentUuid: string): void {
    const component = state.components.find(c => c.uuid === componentUuid)
    if (component) {
      component.is_included = !component.is_included
    }
  }

  function includeComponent(componentUuid: string): void {
    const component = state.components.find(c => c.uuid === componentUuid)
    if (component) {
      component.is_included = true
    }
  }

  function excludeComponent(componentUuid: string): void {
    const component = state.components.find(c => c.uuid === componentUuid)
    if (component) {
      component.is_included = false
    }
  }

  function reorderComponents(newOrder: ResumeComponent[]): void {
    newOrder.forEach((component, index) => {
      component.order_index = index
    })
    state.components = newOrder
  }

  async function refreshPreview(): Promise<void> {
    if (!state.currentResume) return
    state.isGenerating = true
    try {
      const previewUrl = await resumeService.getPDFPreview(state.currentResume.uuid)
      state.previewUrl = previewUrl
    } catch (err) {
      const message = err instanceof Error ? err.message : 'Failed to generate preview'
      state.error = message
      toastError(message, 5000)
    } finally {
      state.isGenerating = false
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
          state.selectedTemplate,
          'My Resume'
        )
        state.currentResume = resume
        state.components = resume.components || []
      } else {
        const updateData: Record<string, unknown> = {
          template_name: state.selectedTemplate,
        }
        const updated = await resumeService.updateResume(state.currentResume.uuid, updateData)
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

  function resetState(): void {
    state.currentResume = null
    state.selectedTemplate = 'MODERN'
    state.components = []
    state.isLoading = false
    state.isSaving = false
    state.isGenerating = false
    state.previewUrl = null
    state.error = null
  }

  return {
    state,
    hasChanges,
    hasResume,
    availableTemplates,
    includedComponents,
    excludedComponents,
    loadResume,
    initEmptyEditor,
    createNewResume,
    updateTemplate,
    toggleComponent,
    includeComponent,
    excludeComponent,
    reorderComponents,
    refreshPreview,
    exportPDF,
    saveResume,
    updateSidebarWidth,
    resetState,
  }
}
