// filepath: frontend/app/stores/profileStore.ts
import { reactive, computed } from 'vue'
import type { Profile } from '~/types/profile'

const state = reactive({
  profiles: [] as Profile[],
  activeProfile: null as Profile | null,
  isLoading: false
})

// Define computeds outside the store function to keep them as singletons
const profiles = computed(() => state.profiles)
const activeProfile = computed(() => state.activeProfile)
const isLoading = computed(() => state.isLoading)

export const useProfileStore = () => {
  return {
    // State
    profiles,
    activeProfile,
    isLoading,

    // Actions
    setProfiles(newProfiles: Profile[]) {
      state.profiles = newProfiles
      
      // If we have an active profile, try to find it in the new list to maintain selection
      if (state.activeProfile) {
        const found = newProfiles.find(p => p.uuid === state.activeProfile?.uuid)
        if (found) {
          state.activeProfile = found
          return
        }
      }

      // Otherwise, default to the first profile or null
      state.activeProfile = newProfiles[0] ?? null
    },

    setActiveProfile(profile: Profile | null) {
      state.activeProfile = profile
    },

    addProfile(profile: Profile) {
      state.profiles.push(profile)
      state.activeProfile = profile
    },

    updateProfile(updatedProfile: Profile) {
      const index = state.profiles.findIndex(p => p.uuid === updatedProfile.uuid)
      if (index !== -1) {
        state.profiles[index] = updatedProfile
      }
      if (state.activeProfile?.uuid === updatedProfile.uuid) {
        state.activeProfile = updatedProfile
      }
    },

    removeProfile(profileId: string) {
      state.profiles = state.profiles.filter(p => p.uuid !== profileId)
      if (state.activeProfile?.uuid === profileId) {
        state.activeProfile = state.profiles[0] ?? null
      }
    },

    setLoading(loading: boolean) {
      state.isLoading = loading
    },

    clearStore() {
      state.profiles = []
      state.activeProfile = null
      state.isLoading = false
    }
  }
}
