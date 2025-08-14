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
              Create your account
            </h1>
            <p class="mt-2 text-gray-600 dark:text-gray-400">
              Start building your perfect resume today
            </p>
          </div>

          <!-- General Error Message -->
          <div v-if="generalError" class="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
            <p class="text-red-700 dark:text-red-400 text-sm">{{ generalError }}</p>
          </div>

          <!-- Form -->
          <form @submit.prevent="handleRegister" class="space-y-6">
            <!-- First Name and Last Name -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <label for="firstName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  First name
                </label>
                <input
                  id="firstName"
                  v-model="firstName"
                  type="text"
                  placeholder="Enter your first name"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
                  :class="firstNameError ? 'border-red-500 dark:border-red-400' : ''"
                  @input="validateFirstName"
                />
                <small v-if="firstNameError" class="text-red-500 text-sm mt-1 block">{{ firstNameError }}</small>
              </div>
              
              <div>
                <label for="lastName" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                  Last name
                </label>
                <input
                  id="lastName"
                  v-model="lastName"
                  type="text"
                  placeholder="Enter your last name"
                  class="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
                  :class="lastNameError ? 'border-red-500 dark:border-red-400' : ''"
                  @input="validateLastName"
                />
                <small v-if="lastNameError" class="text-red-500 text-sm mt-1 block">{{ lastNameError }}</small>
              </div>
            </div>

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
                  placeholder="Create a password"
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
              <!-- Password strength indicator -->
              <div v-if="password" class="mt-2">
                <div class="flex space-x-1">
                  <div class="h-2 flex-1 rounded" :class="passwordStrength >= 1 ? 'bg-red-500' : 'bg-gray-200 dark:bg-gray-700'"></div>
                  <div class="h-2 flex-1 rounded" :class="passwordStrength >= 2 ? 'bg-yellow-500' : 'bg-gray-200 dark:bg-gray-700'"></div>
                  <div class="h-2 flex-1 rounded" :class="passwordStrength >= 3 ? 'bg-green-500' : 'bg-gray-200 dark:bg-gray-700'"></div>
                </div>
                <p class="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {{ passwordStrengthText }}
                </p>
              </div>
              <small v-if="passwordError" class="text-red-500 text-sm mt-1 block">{{ passwordError }}</small>
            </div>

            <!-- Confirm Password -->
            <div>
              <label for="confirmPassword" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Confirm Password
              </label>
              <div class="relative">
                <input
                  id="confirmPassword"
                  v-model="confirmPassword"
                  :type="showConfirmPassword ? 'text' : 'password'"
                  placeholder="Confirm your password"
                  class="w-full px-4 py-3 pr-12 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 transition-colors"
                  :class="confirmPasswordError ? 'border-red-500 dark:border-red-400' : ''"
                  @input="validateConfirmPassword"
                />
                <button
                  type="button"
                  @click="showConfirmPassword = !showConfirmPassword"
                  class="absolute inset-y-0 right-0 pr-3 flex items-center text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
                >
                  <Icon :name="showConfirmPassword ? 'mdi:eye-off' : 'mdi:eye'" class="h-5 w-5" />
                </button>
              </div>
              <small v-if="confirmPasswordError" class="text-red-500 text-sm mt-1 block">{{ confirmPasswordError }}</small>
            </div>

            <!-- Terms and conditions -->
            <div class="flex items-start">
              <input
                v-model="agreeToTerms"
                type="checkbox"
                id="terms"
                class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-800 mt-1"
              />
              <label for="terms" class="ml-2 text-sm text-gray-600 dark:text-gray-400">
                I agree to the 
                <button
                  type="button"
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-500 underline"
                  @click="showTerms = true"
                >
                  Terms of Service
                </button>
                and 
                <button
                  type="button"
                  class="text-blue-600 dark:text-blue-400 hover:text-blue-500 underline"
                  @click="showPrivacy = true"
                >
                  Privacy Policy
                </button>
              </label>
            </div>

            <!-- Submit button -->
            <button
              type="submit"
              :disabled="!agreeToTerms || isLoading"
              class="w-full flex justify-center items-center px-4 py-3 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white font-medium rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Icon v-if="isLoading" name="mdi:loading" class="animate-spin mr-2" />
              {{ isLoading ? 'Creating account...' : 'Create account' }}
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

          <!-- Social signup -->
          <div class="space-y-3">
            <button
              type="button"
              :disabled="isGoogleLoading"
              class="w-full flex justify-center items-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              @click="signupWithGoogle"
            >
              <Icon v-if="isGoogleLoading" name="mdi:loading" class="animate-spin mr-2" />
              <Icon v-else name="mdi:google" class="mr-2" />
              Continue with Google
            </button>
            <button
              type="button"
              :disabled="isGithubLoading"
              class="w-full flex justify-center items-center px-4 py-3 border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-800 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              @click="signupWithGithub"
            >
              <Icon v-if="isGithubLoading" name="mdi:loading" class="animate-spin mr-2" />
              <Icon v-else name="mdi:github" class="mr-2" />
              Continue with GitHub
            </button>
          </div>

          <!-- Sign in link -->
          <div class="text-center">
            <span class="text-gray-600 dark:text-gray-400">Already have an account? </span>
            <button
              type="button"
              class="text-blue-600 dark:text-blue-400 hover:text-blue-500 font-medium underline"
              @click="navigateTo('/login')"
            >
              Sign in
            </button>
          </div>
        </div>
      </div>

      <!-- Right Side - Design/Content -->
      <div class="hidden lg:flex lg:flex-1 auth-split-gradient items-center justify-center p-12">
        <div class="max-w-lg text-center text-white">
          <!-- Logo -->
          <div class="mb-8">
            <Icon name="mdi:rocket-launch" class="text-6xl text-white opacity-90 mx-auto mb-4" />
            <h2 class="text-3xl font-bold">Start Your Journey</h2>
          </div>

          <!-- Content -->
          <div class="space-y-6">
            <h3 class="text-2xl font-semibold">
              Your Dream Job Is Just One Resume Away
            </h3>
            <p class="text-lg opacity-90 leading-relaxed">
              Join over 10,000 professionals who have successfully landed their dream jobs 
              using CAIV's AI-powered resume builder.
            </p>
            
            <!-- Stats -->
            <div class="grid grid-cols-3 gap-4 text-center">
              <div>
                <div class="text-3xl font-bold">98%</div>
                <div class="text-sm opacity-80">Success Rate</div>
              </div>
              <div>
                <div class="text-3xl font-bold">10K+</div>
                <div class="text-sm opacity-80">Users</div>
              </div>
              <div>
                <div class="text-3xl font-bold">5 min</div>
                <div class="text-sm opacity-80">Setup Time</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms of Service Modal -->
    <div
      v-if="showTerms"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showTerms = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] flex flex-col">
        <div class="flex justify-between items-center p-6 border-b dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Terms of Service</h3>
          <button
            @click="showTerms = false"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <Icon name="mdi:close" class="h-5 w-5" />
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1">
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">1. Terms</h3>
            <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              By accessing and using this website, you accept and agree to be bound by the terms and provision of this agreement.
            </p>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">2. Use License</h3>
            <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              Permission is granted to temporarily download one copy of the materials on CAIV's website for personal, non-commercial transitory viewing only.
            </p>
          </div>
        </div>
        
        <div class="flex justify-end p-6 border-t dark:border-gray-700">
          <button
            type="button"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors"
            @click="showTerms = false"
          >
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- Privacy Policy Modal -->
    <div
      v-if="showPrivacy"
      class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50"
      @click.self="showPrivacy = false"
    >
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-2xl w-full max-h-[80vh] flex flex-col">
        <div class="flex justify-between items-center p-6 border-b dark:border-gray-700">
          <h3 class="text-lg font-medium text-gray-900 dark:text-white">Privacy Policy</h3>
          <button
            @click="showPrivacy = false"
            class="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          >
            <Icon name="mdi:close" class="h-5 w-5" />
          </button>
        </div>
        
        <div class="p-6 overflow-y-auto flex-1">
          <div class="space-y-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">Information We Collect</h3>
            <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              We collect information you provide directly to us, such as when you create or modify your account.
            </p>
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100">How We Use Information</h3>
            <p class="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
              We use the information we collect to provide, maintain, and improve our services and develop new features.
            </p>
          </div>
        </div>
        
        <div class="flex justify-end p-6 border-t dark:border-gray-700">
          <button
            type="button"
            class="px-4 py-2 bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white rounded-lg transition-colors"
            @click="showPrivacy = false"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAuthStore } from '~/composables/useAuth'
import type { ApiError } from '~/types/auth'

// Protect this route - only allow guests (redirect authenticated users)
definePageMeta({
  middleware: 'guest'
})

const { register, isLoading: authLoading } = useAuthStore()

// SEO Meta
useSeoMeta({
  title: 'Sign Up - CAIV',
  description: 'Create your CAIV account and start building your perfect AI-powered resume.',
  ogTitle: 'Sign Up - CAIV',
  ogDescription: 'Create your CAIV account and start building your perfect AI-powered resume.',
  ogType: 'website',
  twitterCard: 'summary_large_image',
})

// Form Data
const firstName = ref<string>('')
const lastName = ref<string>('')
const email = ref<string>('')
const password = ref<string>('')
const confirmPassword = ref<string>('')
const showPassword = ref<boolean>(false)
const showConfirmPassword = ref<boolean>(false)
const agreeToTerms = ref<boolean>(false)

// Validation Errors
const firstNameError = ref<string>('')
const lastNameError = ref<string>('')
const emailError = ref<string>('')
const passwordError = ref<string>('')
const confirmPasswordError = ref<string>('')
const generalError = ref<string>('')

// Dialog States
const showTerms = ref<boolean>(false)
const showPrivacy = ref<boolean>(false)

// Loading States
const isLoading = computed(() => authLoading.value)
const isGoogleLoading = ref<boolean>(false)
const isGithubLoading = ref<boolean>(false)

// Email Regex
const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/

// Password Strength
const passwordStrength = computed(() => {
  if (!password.value) return 0
  let strength = 0
  if (password.value.length >= 8) strength++
  if (/[a-z]/.test(password.value)) strength++
  if (/[A-Z]/.test(password.value)) strength++
  if (/\d/.test(password.value)) strength++
  if (/[^a-zA-Z\d]/.test(password.value)) strength++
  return Math.min(strength, 3)
})

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return 'Weak password'
    case 2:
      return 'Medium password'
    case 3:
      return 'Strong password'
    default:
      return ''
  }
})

// Form Validation
const validateFirstName = () => {
  firstNameError.value = ''
  if (!firstName.value) {
    firstNameError.value = 'First name is required'
  } else if (firstName.value.length < 2) {
    firstNameError.value = 'First name must be at least 2 characters'
  }
}

const validateLastName = () => {
  lastNameError.value = ''
  if (!lastName.value) {
    lastNameError.value = 'Last name is required'
  } else if (lastName.value.length < 2) {
    lastNameError.value = 'Last name must be at least 2 characters'
  }
}

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
  } else if (!/(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/.test(password.value)) {
    passwordError.value = 'Password must contain uppercase, lowercase, and number'
  }
}

const validateConfirmPassword = () => {
  confirmPasswordError.value = ''
  if (!confirmPassword.value) {
    confirmPasswordError.value = 'Please confirm your password'
  } else if (confirmPassword.value !== password.value) {
    confirmPasswordError.value = 'Passwords do not match'
  }
}

const validateForm = (): boolean => {
  validateFirstName()
  validateLastName()
  validateEmail()
  validatePassword()
  validateConfirmPassword()
  return !firstNameError.value && !lastNameError.value && !emailError.value && !passwordError.value && !confirmPasswordError.value && agreeToTerms.value
}

// Handle Registration
const handleRegister = async () => {
  if (!validateForm()) return

  generalError.value = ''

  try {
    await register({
      email: email.value,
      password: password.value,
      confirm_password: confirmPassword.value,
      first_name: firstName.value,
      last_name: lastName.value
    })
    // Navigation will be handled by the auth store after successful registration
  } catch (error: any) {
    generalError.value = error.statusMessage || error.message || 'Failed to create account. Please try again.'
  }
}

// Social Signup Handlers
const signupWithGoogle = async () => {
  isGoogleLoading.value = true
  try {
    // TODO: Implement Google OAuth
    console.log('Signup with Google')
  } catch (error: any) {
    generalError.value = 'Failed to signup with Google. Please try again.'
  } finally {
    isGoogleLoading.value = false
  }
}

const signupWithGithub = async () => {
  isGithubLoading.value = true
  try {
    // TODO: Implement GitHub OAuth
    console.log('Signup with GitHub')
  } catch (error: any) {
    generalError.value = 'Failed to signup with GitHub. Please try again.'
  } finally {
    isGithubLoading.value = false
  }
}
</script>