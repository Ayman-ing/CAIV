<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Navigation -->
    <SectionsNavigation />
    
    <!-- Split Screen Layout -->
    <div class="flex min-h-screen pt-16">
      <!-- Left Side - Form -->
      <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900">
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
                @input="validateEmail"
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
                  @input="validatePassword"
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

            <!-- Remember me & Forgot password -->
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
                @click="showForgotPassword = true"
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
              @click="navigateTo('/register')"
            >
              Sign up
            </button>
          </div>
        </div>
      </div>

      <!-- Right Side - Design/Content -->
      <div class="hidden lg:flex lg:flex-1 auth-split-gradient items-center justify-center p-12">
        <div class="max-w-lg text-center text-white">
          <!-- Logo -->
          <div class="mb-8">
            <Icon name="mdi:file-document-edit" class="text-6xl text-white opacity-90 mx-auto mb-4" />
            <h2 class="text-3xl font-bold">CAIV</h2>
          </div>

          <!-- Content -->
          <div class="space-y-6">
            <h3 class="text-2xl font-semibold">
              Build Your Perfect Resume with AI
            </h3>
            <p class="text-lg opacity-90 leading-relaxed">
              Join thousands of professionals who use CAIV to create stunning, 
              ATS-friendly resumes that get noticed by employers.
            </p>
            
            <!-- Features -->
            <div class="space-y-4 text-left">
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-300 text-xl" />
                <span>AI-powered resume optimization</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:lightning-bolt" class="text-yellow-300 text-xl" />
                <span>Professional templates</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:shield-check" class="text-blue-300 text-xl" />
                <span>ATS-friendly formatting</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Forgot Password Modal -->
    <div
      v-if="showForgotPassword"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showForgotPassword = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full p-6">
        <div class="flex justify-between items-center mb-4">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Reset Password</h3>
          <button
            @click="showForgotPassword = false"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <Icon name="mdi:close" class="h-5 w-5" />
          </button>
        </div>
        
        <div class="space-y-4">
          <p class="text-gray-600 dark:text-gray-300">
            Enter your email address and we'll send you a link to reset your password.
          </p>
          <input
            v-model="forgotEmail"
            type="email"
            placeholder="Enter your email"
            class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
          />
        </div>
        
        <div class="flex justify-end space-x-2 mt-6">
          <button
            type="button"
            class="px-4 py-2 text-gray-600 dark:text-gray-400 hover:text-gray-800 dark:hover:text-gray-200"
            @click="showForgotPassword = false"
          >
            Cancel
          </button>
          <button
            type="button"
            :disabled="!forgotEmail || isForgotLoading"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center"
            @click="handleForgotPassword"
          >
            <Icon v-if="isForgotLoading" name="mdi:loading" class="animate-spin mr-2" />
            {{ isForgotLoading ? 'Sending...' : 'Send Reset Link' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/composables/useAuth'

// Protect this route - only allow guests (redirect authenticated users)
definePageMeta({
  middleware: 'guest'
})

const { login, isLoading: authLoading } = useAuthStore()

// SEO Meta
useSeoMeta({
  title: 'Sign In - CAIV',
  description: 'Sign in to your CAIV account and continue building your perfect AI-powered resume.',
  ogTitle: 'Sign In - CAIV',
  ogDescription: 'Sign in to your CAIV account and continue building your perfect AI-powered resume.',
  ogType: 'website',
  twitterCard: 'summary_large_image',
})

// Form Data
const email = ref<string>('')
const password = ref<string>('')
const showPassword = ref<boolean>(false)
const rememberMe = ref<boolean>(false)
const forgotEmail = ref<string>('')

// Validation Errors
const emailError = ref<string>('')
const passwordError = ref<string>('')
const generalError = ref<string>('')
const showForgotPassword = ref<boolean>(false)

// Loading States
const isLoading = computed(() => authLoading.value)
const isGoogleLoading = ref<boolean>(false)
const isGithubLoading = ref<boolean>(false)
const isForgotLoading = ref<boolean>(false)

// Email Regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Form Validation
const validateEmail = () => {
  emailError.value = ''
  if (!email.value) {
    emailError.value = 'Email is required'
  } else if (!emailRegex.test(email.value)) {
    emailError.value = 'Please enter a valid email'
  }
}

const validatePassword = () => {
  passwordError.value = ''
  if (!password.value) {
    passwordError.value = 'Password is required'
  } else if (password.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters'
  }
}

const validateForm = (): boolean => {
  validateEmail()
  validatePassword()
  return !emailError.value && !passwordError.value
}

// Handle Login
const handleLogin = async () => {
  if (!validateForm()) return

  generalError.value = ''

  try {
    await login({
      email: email.value,
      password: password.value
    })
    // Navigation will be handled by the auth store after successful login
  } catch (error: any) {
    generalError.value = error.message || 'Invalid credentials. Please try again.'
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

// Forgot Password Handler
const handleForgotPassword = async () => {
  if (!forgotEmail.value) return

  isForgotLoading.value = true
  try {
    // TODO: Implement forgot password API call
    console.log('Sending reset email to:', forgotEmail.value)
    showForgotPassword.value = false
    forgotEmail.value = ''
  } catch (error: any) {
    generalError.value = 'Failed to send reset email. Please try again.'
  } finally {
    isForgotLoading.value = false
  }
}
</script>