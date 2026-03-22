// filepath: frontend/app/services/profileService.ts
import { profileApi } from '~/api/profile'
import { useProfileStore } from '~/stores/profileStore'
import { useUserStore } from '~/stores/userStore'
import type { ProfileCreate, ProfileUpdate } from '~/types/profile'

export const profileService = {
  async fetchUserProfiles(): Promise<void> {
    const profileStore = useProfileStore()
    const userStore = useUserStore()
    
    if (!userStore.user.value?.uuid) return

    profileStore.setLoading(true)
    try {
      const profiles = await profileApi.getProfiles(userStore.user.value.uuid)
      profileStore.setProfiles(profiles)
    } catch (error) {
      console.error('Failed to fetch profiles:', error)
      throw error
    } finally {
      profileStore.setLoading(false)
    }
  },

  async createProfile(data: ProfileCreate): Promise<void> {
    const profileStore = useProfileStore()
    const userStore = useUserStore()
    
    if (!userStore.user.value?.uuid) throw new Error('User not logged in')

    profileStore.setLoading(true)
    try {
      const newProfile = await profileApi.createProfile(userStore.user.value.uuid, data)
      profileStore.addProfile(newProfile)
    } catch (error) {
      throw error
    } finally {
      profileStore.setLoading(false)
    }
  },

  async updateProfile(profileId: string, data: ProfileUpdate): Promise<void> {
    const profileStore = useProfileStore()
    const userStore = useUserStore()
    
    if (!userStore.user.value?.uuid) throw new Error('User not logged in')

    profileStore.setLoading(true)
    try {
      const updatedProfile = await profileApi.updateProfile(userStore.user.value.uuid, profileId, data)
      profileStore.updateProfile(updatedProfile)
    } catch (error) {
      throw error
    } finally {
      profileStore.setLoading(false)
    }
  },
  
  async deleteProfile(profileId: string): Promise<void> {
    const profileStore = useProfileStore()
    const userStore = useUserStore()
    
    if (!userStore.user.value?.uuid) throw new Error('User not logged in')

    profileStore.setLoading(true)
    try {
      await profileApi.deleteProfile(userStore.user.value.uuid, profileId)
      profileStore.removeProfile(profileId)
    } catch (error) {
      throw error
    } finally {
      profileStore.setLoading(false)
    }
  }
}
