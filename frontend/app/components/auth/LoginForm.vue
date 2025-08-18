<script setup lang="ts">
import { authService } from '~/services/authService'
import { useUserStore } from '~/stores/userStore'
import type { ApiError } from '~/types/auth'

// Define emits
defineEmits<{
  'forgot-password': []
  'switch-to-register': []
}>()

const store = useUserStore()

// Form Data
const email = ref<string>('')
const password = ref<string>('')
const showPassword = ref<boolean>(false)
const rememberMe = ref<boolean>(false)

// Validation Errors
const emailError = ref<string>('')
const passwordError = ref<string>('')
const generalError = ref<string>('')

// Loading States
const isGoogleLoading = ref<boolean>(false)
const isGithubLoading = ref<boolean>(false)

// Get loading state from store
const isLoading = computed(() => store.isLoading.value)

// Validation Functions
const validateEmail = (email: string): string => {
  if (!email.trim()) {
    return 'Email is required'
  }
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!emailRegex.test(email)) {
    return 'Please enter a valid email address'
  }
  return ''
}

const validatePassword = (password: string): string => {
  if (!password) {
    return 'Password is required'
  }
  return ''
}

// Form Validation
const validateEmailField = () => {
  emailError.value = validateEmail(email.value)
}

const validatePasswordField = () => {
  passwordError.value = validatePassword(password.value)
}

const validateForm = (): boolean => {
  validateEmailField()
  validatePasswordField()
  return !emailError.value && !passwordError.value
}

// Handle Login
const handleLogin = async () => {
  if (!validateForm()) return

  generalError.value = ''

  try {
    await authService.login({
      email: email.value,
      password: password.value
    })
    // Navigation will be handled by the auth service
  } catch (error: any) {
    generalError.value = error.statusMessage || error.message || 'Failed to sign in. Please try again.'
  }
}

// Social Login Handlers
const loginWithGoogle = async () => {
  isGoogleLoading.value = true
  try {
    // TODO: Implement Google OAuth
    console.log('Login with Google')
  } catch (error: any) {
    generalError.value = 'Failed to login with Google. Please try again.'
  } finally {
    isGoogleLoading.value = false
  }
}

const loginWithGithub = async () => {
  isGithubLoading.value = true
  try {
    // TODO: Implement GitHub OAuth
    console.log('Login with GitHub')
  } catch (error: any) {
    generalError.value = 'Failed to login with GitHub. Please try again.'
  } finally {
    isGithubLoading.value = false
  }
}
</script>

<template>
  <div class="w-full max-w-md space-y-8">
    <!-- Header -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
        Welcome back
      </h1>
      <p class="mt-2 text-gray-600 dark:text-gray-400">
        Sign in to your account to continue
      </p>
    </div>

    <!-- General Error Message -->
    <div v-if="generalError" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
      <p class="text-red-700 dark:text-red-400 text-sm">{{ generalError }}</p>
    </div>

    <!-- Form -->
    <form @submit.prevent="handleLogin" class="space-y-6">
      <!-- Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Email address
        </label>
        <input
          id="email"
          v-model="email"
          type="email"
          placeholder="Enter your email"
          class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
          :class="emailError ? 'border-red-500 dark:border-red-400' : ''"
          @input="validateEmailField"
        />
        <small v-if="emailError" class="text-red-500 text-sm mt-1 block">{{ emailError }}</small>
      </div>

      <!-- Password -->
      <div>
        <label for="password" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Password
        </label>
        <div class="relative">
          <input
            id="password"
            v-model="password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Enter your password"
            class="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
            :class="passwordError ? 'border-red-500 dark:border-red-400' : ''"
            @input="validatePasswordField"
          />
          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <Icon :name="showPassword ? 'mdi:eye-off' : 'mdi:eye'" class="h-5 w-5" />
          </button>
        </div>
        <small v-if="passwordError" class="text-red-500 text-sm mt-1 block">{{ passwordError }}</small>
      </div>

      <!-- Remember me and Forgot password -->
      <div class="flex items-center justify-between">
        <div class="flex items-center">
          <input
            v-model="rememberMe"
            type="checkbox"
            id="remember"
            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800"
          />
          <label for="remember" class="ml-2 text-sm text-gray-600 dark:text-gray-400">
            Remember me
          </label>
        </div>
        <button
          type="button"
          class="text-sm text-blue-600 dark:text-blue-400 hover:text-blue-500 underline"
          @click="$emit('forgot-password')"
        >
          Forgot password?
        </button>
      </div>

      <!-- Submit button -->
      <button
        type="submit"
        :disabled="isLoading"
        class="w-full flex justify-center items-center px-4 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
      >
        <Icon v-if="isLoading" name="mdi:loading" class="animate-spin mr-2" />
        {{ isLoading ? 'Signing in...' : 'Sign in' }}
      </button>
    </form>

    <!-- Divider -->
    <div class="relative">
      <div class="absolute inset-0 flex items-center">
        <div class="w-full border-t border-gray-300 dark:border-gray-600"></div>
      </div>
      <div class="relative flex justify-center text-sm">
        <span class="px-2 bg-white dark:bg-gray-900 text-gray-500 dark:text-gray-400">Or continue with</span>
      </div>
    </div>

    <!-- Social login -->
    <div class="space-y-3">
      <button
        type="button"
        :disabled="isGoogleLoading"
        class="w-full flex justify-center items-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        @click="loginWithGoogle"
      >
        <Icon v-if="isGoogleLoading" name="mdi:loading" class="animate-spin mr-2" />
        <Icon v-else name="mdi:google" class="mr-2" />
        Continue with Google
      </button>
      <button
        type="button"
        :disabled="isGithubLoading"
        class="w-full flex justify-center items-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
        @click="loginWithGithub"
      >
        <Icon v-if="isGithubLoading" name="mdi:loading" class="animate-spin mr-2" />
        <Icon v-else name="mdi:github" class="mr-2" />
        Continue with GitHub
      </button>
    </div>

    <!-- Sign up link -->
    <div class="text-center">
      <span class="text-gray-600 dark:text-gray-400">Don't have an account? </span>
      <button
        type="button"
        class="text-blue-600 dark:text-blue-400 hover:text-blue-500 font-medium underline"
        @click="$emit('switch-to-register')"
      >
        Sign up
      </button>
    </div>
  </div>
</template>


