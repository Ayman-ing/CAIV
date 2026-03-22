// filepath: frontend/app/stores/profileStore.ts
import { reactive, computed, readonly } from 'vue'
import type { Profile } from '~/types/profile'

const state = reactive({
  profiles: [] as Profile[],
  activeProfile: null as Profile | null,
  isLoading: false
})

export const useProfileStore = () => {
  return {
    // State
    profiles: computed(() => state.profiles),
    activeProfile: computed(() => state.activeProfile),
    isLoading: computed(() => state.isLoading),

    // Actions
    setProfiles(profiles: Profile[]) {
      state.profiles = profiles
      if (profiles.length > 0 && !state.activeProfile) {
        state.activeProfile = profiles[0] || null
      }
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
        state.activeProfile = state.profiles.length > 0 ? (state.profiles[0] || null) : null
      }
    },
    setLoading(loading: boolean) {
      state.isLoading = loading
    }
  }
}
