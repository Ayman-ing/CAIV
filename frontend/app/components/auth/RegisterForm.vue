<script setup lang="ts">
import { authService } from '~/services/authService'
import { useUserStore } from '~/stores/userStore'
import type { ApiError } from '~/types/auth'

// Define emits
defineEmits<{
  'show-terms': []
  'show-privacy': []
  'switch-to-login': []
}>()

const store = useUserStore()

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

// Loading States
const isGoogleLoading = ref<boolean>(false)
const isGithubLoading = ref<boolean>(false)

// Get loading state from store
const isLoading = computed(() => store.isLoading.value)

// Password Strength
const passwordStrength = computed(() => {
  if (!password.value) return 0
  
  let strength = 0
  if (password.value.length >= 8) strength++
  if (/[a-z]/.test(password.value)) strength++
  if (/[A-Z]/.test(password.value)) strength++
  if (/\d/.test(password.value)) strength++
  if (/[^A-Za-z0-9]/.test(password.value)) strength++
  
  return Math.min(strength, 3)
})

const passwordStrengthText = computed(() => {
  switch (passwordStrength.value) {
    case 0:
    case 1:
      return 'Weak'
    case 2:
      return 'Medium'
    case 3:
      return 'Strong'
    default:
      return 'Weak'
  }
})

// Event Handlers with inline validation
const handleFirstNameInput = () => {
  if (!firstName.value.trim()) {
    firstNameError.value = 'First name is required'
  } else if (firstName.value.trim().length < 2) {
    firstNameError.value = 'First name must be at least 2 characters long'
  } else {
    firstNameError.value = ''
  }
}

const handleLastNameInput = () => {
  if (!lastName.value.trim()) {
    lastNameError.value = 'Last name is required'
  } else if (lastName.value.trim().length < 2) {
    lastNameError.value = 'Last name must be at least 2 characters long'
  } else {
    lastNameError.value = ''
  }
}

const handleEmailInput = () => {
  if (!email.value.trim()) {
    emailError.value = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    emailError.value = 'Please enter a valid email address'
  } else {
    emailError.value = ''
  }
}

const handlePasswordInput = () => {
  if (!password.value) {
    passwordError.value = 'Password is required'
  } else if (password.value.length < 8) {
    passwordError.value = 'Password must be at least 8 characters long'
  } else if (!/(?=.*[a-z])/.test(password.value)) {
    passwordError.value = 'Password must contain at least one lowercase letter'
  } else if (!/(?=.*[A-Z])/.test(password.value)) {
    passwordError.value = 'Password must contain at least one uppercase letter'
  } else if (!/(?=.*\d)/.test(password.value)) {
    passwordError.value = 'Password must contain at least one number'
  } else {
    passwordError.value = ''
  }
}

const handleConfirmPasswordInput = () => {
  if (!confirmPassword.value) {
    confirmPasswordError.value = 'Please confirm your password'
  } else if (password.value !== confirmPassword.value) {
    confirmPasswordError.value = 'Passwords do not match'
  } else {
    confirmPasswordError.value = ''
  }
}

const validateForm = (): boolean => {
  handleFirstNameInput()
  handleLastNameInput()
  handleEmailInput()
  handlePasswordInput()
  handleConfirmPasswordInput()
  return !firstNameError.value && !lastNameError.value && !emailError.value && !passwordError.value && !confirmPasswordError.value && agreeToTerms.value
}

// Handle Registration
const handleRegister = async () => {
  if (!validateForm()) return

  generalError.value = ''

  try {
    await authService.register({
      email: email.value,
      password: password.value,
      confirm_password: confirmPassword.value,
      first_name: firstName.value,
      last_name: lastName.value
    })
    // Navigation will be handled by the auth service
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


<template>
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
            @input="handleFirstNameInput"
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
            @input="handleLastNameInput"
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
          @input="handleEmailInput"
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
            @input="handlePasswordInput"
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
            @input="handleConfirmPasswordInput"
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
            @click="$emit('show-terms')"
          >
            Terms of Service
          </button>
          and 
          <button
            type="button"
            class="text-blue-600 dark:text-blue-400 hover:text-blue-500 underline"
            @click="$emit('show-privacy')"
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
        @click="$emit('switch-to-login')"
      >
        Sign in
      </button>
    </div>
  </div>
</template>

