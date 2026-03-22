// filepath: frontend/app/api/profile.ts
import type { Profile, ProfileCreate, ProfileUpdate } from '~/types/profile'

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

export const profileApi = {
  async getProfiles(userId: string): Promise<Profile[]> {
    return await $fetch<Profile[]>(getApiUrl('/api/v1/profiles/'), {
      method: 'GET',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  },

  async getProfile(userId: string, profileId: string): Promise<Profile> {
    return await $fetch<Profile>(getApiUrl(`/api/v1/profiles/${profileId}`), {
      method: 'GET',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  },

  async createProfile(userId: string, data: ProfileCreate): Promise<Profile> {
    return await $fetch<Profile>(getApiUrl('/api/v1/profiles/'), {
      method: 'POST',
      query: { user_uuid: userId },
      body: data,
      headers: getAuthHeaders(),
    })
  },

  async updateProfile(userId: string, profileId: string, data: ProfileUpdate): Promise<Profile> {
    return await $fetch<Profile>(getApiUrl(`/api/v1/profiles/${profileId}`), {
      method: 'PUT',
      query: { user_uuid: userId },
      body: data,
      headers: getAuthHeaders(),
    })
  },

  async deleteProfile(userId: string, profileId: string): Promise<{ message: string }> {
    return await $fetch<{ message: string }>(getApiUrl(`/api/v1/profiles/${profileId}`), {
      method: 'DELETE',
      query: { user_uuid: userId },
      headers: getAuthHeaders(),
    })
  }
}
