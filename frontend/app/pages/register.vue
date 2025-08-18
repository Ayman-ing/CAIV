<template>
  <div class="min-h-screen bg-white dark:bg-gray-900">
    <!-- Navigation -->
    <SectionsNavigation />
    
    <!-- Split Screen Layout -->
    <div class="flex min-h-screen pt-16">
      <!-- Left Side - Form -->
      <div class="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8 bg-white dark:bg-gray-900">
        <AuthRegisterForm 
          @switch-to-login="navigateTo('/login')"
          @show-terms="showTermsModal = true"
          @show-privacy="showPrivacyModal = true"
        />
      </div>

      <!-- Right Side - Background/Marketing -->
      <div class="hidden lg:block flex-1 relative bg-gradient-to-br from-blue-600 to-purple-700">
        <div class="absolute inset-0 bg-black/20"></div>
        <div class="relative flex flex-col justify-center h-full px-12">
          <div class="space-y-6 text-white">
            <h2 class="text-4xl font-bold">Join thousands of professionals</h2>
            <p class="text-xl text-blue-100">
              Create stunning resumes with our AI-powered builder and land your dream job.
            </p>
            <div class="space-y-4">
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>AI-powered resume optimization</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Professional templates</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>ATS-friendly formats</span>
              </div>
              <div class="flex items-center space-x-3">
                <Icon name="mdi:check-circle" class="text-green-400 text-xl" />
                <span>Real-time collaboration</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Terms Modal -->
    <div v-if="showTermsModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Terms of Service</h3>
            <button @click="showTermsModal = false" class="text-gray-400 hover:text-gray-600">
              <Icon name="mdi:close" class="text-xl" />
            </button>
          </div>
          <div class="text-gray-600 dark:text-gray-300 text-sm space-y-4">
            <p>Welcome to AI Resume Builder. By using our service, you agree to these terms.</p>
            <p><strong>Account Registration:</strong> You must provide accurate information when creating your account.</p>
            <p><strong>Use of Service:</strong> Our AI-powered tools are designed to help you create professional resumes.</p>
            <p><strong>Privacy:</strong> We protect your data according to our Privacy Policy.</p>
            <p><strong>Limitation of Liability:</strong> We strive to provide the best service but cannot guarantee uninterrupted access.</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Privacy Modal -->
    <div v-if="showPrivacyModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-50">
      <div class="bg-white dark:bg-gray-800 rounded-lg max-w-2xl w-full mx-4 max-h-96 overflow-y-auto">
        <div class="p-6">
          <div class="flex justify-between items-center mb-4">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-white">Privacy Policy</h3>
            <button @click="showPrivacyModal = false" class="text-gray-400 hover:text-gray-600">
              <Icon name="mdi:close" class="text-xl" />
            </button>
          </div>
          <div class="text-gray-600 dark:text-gray-300 text-sm space-y-4">
            <p>Your privacy is important to us. This policy explains how we collect and use your information.</p>
            <p><strong>Data Collection:</strong> We collect information you provide during registration and resume building.</p>
            <p><strong>Data Use:</strong> We use your data to provide and improve our services.</p>
            <p><strong>Data Security:</strong> We implement security measures to protect your information.</p>
            <p><strong>Data Sharing:</strong> We do not sell your personal information to third parties.</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  middleware: 'guest'
})

// Modal states
const showTermsModal = ref<boolean>(false)
const showPrivacyModal = ref<boolean>(false)
</script>
