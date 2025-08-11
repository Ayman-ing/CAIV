// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: [
    '@nuxtjs/tailwindcss',
    '@nuxt/eslint',
    '@nuxt/icon',
    '@primevue/nuxt-module'
  ],
  css : [
    '@/assets/css/main.css'
  ],
  primevue: {
    options: {
      theme: {
        preset: 'lara-light-blue',
      }
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE_URL || 'http://localhost:8000',
    }
  },
  ssr : false,
})