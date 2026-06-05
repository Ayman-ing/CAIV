import { resumeDraftApi } from '~/api/resumeDraft'

export interface DraftData {
  components: any[]
  profileData: any
  selectedTemplate: string
}

export const resumeDraftService = {
  async saveDraft(
    profileId: string,
    draftUuid: string | null,
    title: string,
    state: { components: any[]; profileData: any; selectedTemplate: string }
  ): Promise<{ uuid: string; title: string }> {
    const draftData: DraftData = {
      components: state.components,
      profileData: state.profileData,
      selectedTemplate: state.selectedTemplate,
    }

    if (draftUuid) {
      const result = await resumeDraftApi.updateDraft(profileId, draftUuid, {
        title,
        draft_data: draftData as unknown as Record<string, any>,
      })
      return { uuid: result.uuid, title: result.title }
    } else {
      const result = await resumeDraftApi.createDraft(
        profileId,
        title,
        state.selectedTemplate,
        draftData as unknown as Record<string, any>
      )
      return { uuid: result.uuid, title: result.title }
    }
  },

  async loadDraft(profileId: string, draftUuid: string): Promise<{
    components: any[]
    profileData: any
    selectedTemplate: string
    title: string
  }> {
    const result = await resumeDraftApi.getDraft(profileId, draftUuid)
    const data = result.draft_data as unknown as DraftData
    return {
      components: data.components || [],
      profileData: data.profileData || {},
      selectedTemplate: data.selectedTemplate || 'CANADIAN',
      title: result.title,
    }
  },

  async listDrafts(profileId: string) {
    return await resumeDraftApi.listDrafts(profileId)
  },

  async deleteDraft(profileId: string, draftUuid: string) {
    await resumeDraftApi.deleteDraft(profileId, draftUuid)
  },
}
