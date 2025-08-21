<script setup lang="ts">
// filepath: frontend/app/components/dashboard/DashboardHome.vue
import JobInputCard from './JobInputCard.vue'
import ResumePreviewCard from './ResumePreviewCard.vue'
import { useUserStore } from '~/stores/userStore'
const { user } = useUserStore()

// Navigation methods
const navigateToSections = () => navigateTo('/profile/sections')
const navigateToExtractResume = () => navigateTo('/profile/extract-resume')  
const navigateToLinkedIn = () => navigateTo('/profile/extract-linkedin')
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <!-- Full width container -->
    <div class="mx-auto px-4 sm:px-6 lg:px-8 xl:px-12 2xl:px-16 max-w-none">
      
      <!-- Main Dashboard Grid -->
      <div class="grid grid-cols-1 xl:grid-cols-4 2xl:grid-cols-5 gap-8">
        
        <!-- Main Content Area - Takes most space -->
        <div class="xl:col-span-3 2xl:col-span-4 space-y-8">
          
          <!-- Step 1: Enhance Your Profile -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-8">
            <div class="flex items-center mb-6">
              <div class="flex-shrink-0 w-8 h-8 bg-purple-500 dark:bg-purple-400 text-white rounded-full flex items-center justify-center font-semibold">
                1
              </div>
              <h2 class="ml-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Enhance Your Profile</h2>
            </div>
            
            <p class="text-gray-600 dark:text-gray-400 mb-8">
              Build a comprehensive profile that will serve as the foundation for all your AI-generated resumes.
            </p>
            
            <!-- Three horizontal action buttons -->
            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
              <button
                @click="navigateToSections"
                class="flex flex-col items-center p-6 bg-gradient-to-br from-purple-100 to-purple-200 dark:from-purple-900/30 dark:to-purple-800/30 border border-purple-300 dark:border-purple-700 rounded-lg hover:from-purple-200 hover:to-purple-300 dark:hover:from-purple-800/40 dark:hover:to-purple-700/40 transition-all duration-200 group"
              >
                <div class="p-4 bg-purple-500 dark:bg-purple-600 text-white rounded-xl mb-4 group-hover:bg-purple-600 dark:group-hover:bg-purple-500 transition-colors">
                  <Icon name="heroicons:plus-circle" class="w-8 h-8" />
                </div>
                <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">Add Profile Sections</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
                  Add work experience, education, skills, and other professional details
                </p>
              </button>

              <button
                @click="navigateToExtractResume"
                class="flex flex-col items-center p-6 bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 border border-green-300 dark:border-green-700 rounded-lg hover:from-green-200 hover:to-green-300 dark:hover:from-green-800/40 dark:hover:to-green-700/40 transition-all duration-200 group"
              >
                <div class="p-4 bg-green-500 dark:bg-green-600 text-white rounded-xl mb-4 group-hover:bg-green-600 dark:group-hover:bg-green-500 transition-colors">
                  <Icon name="heroicons:document-arrow-up" class="w-8 h-8" />
                </div>
                <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">Extract from Resume</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
                  Upload your existing resume to automatically extract your professional data
                </p>
              </button>

              <button
                @click="navigateToLinkedIn"
                class="flex flex-col items-center p-6 bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 border border-blue-300 dark:border-blue-700 rounded-lg hover:from-blue-200 hover:to-blue-300 dark:hover:from-blue-800/40 dark:hover:to-blue-700/40 transition-all duration-200 group"
              >
                <div class="p-4 bg-blue-500 dark:bg-blue-600 text-white rounded-xl mb-4 group-hover:bg-blue-600 dark:group-hover:bg-blue-500 transition-colors">
                  <Icon name="mdi:linkedin" class="w-8 h-8" />
                </div>
                <h3 class="font-semibold text-gray-900 dark:text-gray-100 mb-2">Import LinkedIn Profile</h3>
                <p class="text-sm text-gray-600 dark:text-gray-400 text-center">
                  Import your professional information directly from your LinkedIn profile
                </p>
              </button>
            </div>
          </div>

          <!-- Step 2: Paste Job Description -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-8">
            <div class="flex items-center mb-6">
              <div class="flex-shrink-0 w-8 h-8 bg-blue-500 dark:bg-blue-400 text-white rounded-full flex items-center justify-center font-semibold">
                2
              </div>
              <h2 class="ml-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">Paste Job Description</h2>
            </div>
            
            <JobInputCard />
          </div>

            <!-- Recent Resumes -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-6">
            <div class="flex items-center mb-6">
              <div class="flex-shrink-0 w-8 h-8 bg-green-500 dark:bg-green-400 text-white rounded-full flex items-center justify-center font-semibold">
                3
              </div>
              <h2 class="ml-4 text-2xl font-semibold text-gray-900 dark:text-gray-100">View Generated Resume</h2>
            </div>
            <ResumePreviewCard />
          </div>
         
        </div>

        <!-- Right Sidebar -->
        <div class="xl:col-span-1 space-y-6">
       

          <!-- Quick Tips -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-6">
            <h3 class="text-lg font-semibold text-gray-900 dark:text-gray-100 mb-4">💡 Quick Tips</h3>
            <div class="space-y-4 text-sm">
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-blue-500 dark:bg-blue-400 rounded-full mt-1.5 flex-shrink-0"></div>
                <p class="text-gray-600 dark:text-gray-400">
                  <strong class="text-gray-900 dark:text-gray-100">Complete your profile first</strong> - The more details you provide, the better our AI can tailor your resume.
                </p>
              </div>
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-green-500 dark:bg-green-400 rounded-full mt-1.5 flex-shrink-0"></div>
                <p class="text-gray-600 dark:text-gray-400">
                  <strong class="text-gray-900 dark:text-gray-100">Copy full job descriptions</strong> - Include requirements, responsibilities, and company info for best results.
                </p>
              </div>
              <div class="flex items-start space-x-3">
                <div class="w-2 h-2 bg-purple-500 dark:bg-purple-400 rounded-full mt-1.5 flex-shrink-0"></div>
                <p class="text-gray-600 dark:text-gray-400">
                  <strong class="text-gray-900 dark:text-gray-100">Review and customize</strong> - Always review the generated resume and make personal adjustments.
                </p>
              </div>
            </div>
          </div>
          <!-- Not yet decided -->
          <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-6">
            <div class="space-y-4 h-80">
              <!-- TODO : add a section -->
            </div>
          </div>
        </div>
       
      </div>
    </div>
  </div>
</template>