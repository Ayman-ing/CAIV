<script setup lang="ts">
// Components
import JobInputCard from './JobInputCard.vue'
import ResumePreviewCard from './ResumePreviewCard.vue'

// Stores
import { useUserStore } from '~/stores/userStore'
const userStore = useUserStore()

// Types
interface JobAnalysisResult {
  title: string
  company: string
  matchPercentage: number
  highlights: string[]
  emphasizedSkills: string[]
  resumeContent?: string
}

// State
const showResumeModal = ref<boolean>(false)
const selectedResume = ref<any>(null)
const currentJob = ref<JobAnalysisResult | null>(null)

// Navigation methods for profile actions
const navigateToAddSections = () => {
  navigateTo('/profile/sections')
}

const navigateToExtractFromResume = () => {
  navigateTo('/profile/extract-resume')
}

const navigateToExtractFromLinkedIn = () => {
  navigateTo('/profile/extract-linkedin')
}

// Methods
const handleJobAnalyzed = (jobData: any) => {
  // Simulate AI processing result
  currentJob.value = {
    title: jobData.jobTitle,
    company: jobData.company,
    matchPercentage: Math.floor(Math.random() * (95 - 75) + 75), // 75-95%
    highlights: [
      'Emphasized relevant technical skills from your experience',
      'Highlighted matching project experience',
      'Tailored professional summary for the role',
      'Optimized keywords for ATS compatibility'
    ],
    emphasizedSkills: jobData.requirements.slice(0, 8)
  }
  
  // Scroll to the results
  nextTick(() => {
    const resultsElement = document.querySelector('[data-step="2"]')
    if (resultsElement) {
      resultsElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  })
}

const handleResumeSelect = (resume: any) => {
  selectedResume.value = resume
  showResumeModal.value = true
}

const scrollToJobInput = () => {
  const jobInputElement = document.querySelector('[data-step="1"]')
  if (jobInputElement) {
    jobInputElement.scrollIntoView({ behavior: 'smooth', block: 'start' })
  }
}

const previewResume = () => {
  if (currentJob.value) {
    selectedResume.value = {
      id: 'current',
      jobTitle: currentJob.value.title,
      company: currentJob.value.company,
      matchPercentage: currentJob.value.matchPercentage,
      content: currentJob.value.resumeContent || 'Resume content would be displayed here...'
    }
    showResumeModal.value = true
  }
}

const downloadResume = () => {
  // TODO: Implement actual resume download
  console.log('Downloading resume for:', currentJob.value)
  
  // Simulate download
  const link = document.createElement('a')
  link.href = '#' // This would be the actual PDF URL
  link.download = `${currentJob.value?.company}_${currentJob.value?.title}_Resume.pdf`
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
}

const saveResume = async () => {
  if (!currentJob.value) return
  
  try {
    // TODO: Save resume to database/store
    console.log('Saving resume:', currentJob.value)
    
    // Show success message
    alert('Resume saved successfully!')
    
    // Clear current job to allow new generation
    currentJob.value = null
    
  } catch (error) {
    console.error('Error saving resume:', error)
    alert('Error saving resume. Please try again.')
  }
}

// Load dashboard data on mount
onMounted(() => {
  // TODO: Load user stats, recent resumes, etc.
  console.log('Loading dashboard data...')
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Welcome Header -->
    <div class="mb-8">
      <div class="text-center">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white mb-2">
          Welcome back, {{ userStore.userName || 'User' }}! 👋
        </h1>
        <p class="text-lg text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
          Create tailored resumes for every job opportunity with AI-powered analysis
        </p>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
      <!-- Left Column - Main Workflow -->
      <div class="lg:col-span-2 space-y-8">
        <!-- Step 1: Enhance Your Profile -->
        <div class="relative">
          <div class="absolute -left-4 top-8 w-8 h-8 bg-purple-600 text-white rounded-full flex items-center justify-center text-sm font-bold z-10">
            1
          </div>
          
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-300 dark:border-gray-700 p-6">
            <div class="flex items-center mb-6">
              <div class="p-3 bg-purple-100 dark:bg-purple-900/30 rounded-full mr-4">
                <Icon name="mdi:account-plus" class="text-2xl text-purple-700 dark:text-purple-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  Enhance Your Profile
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  Build a comprehensive profile for better resume matching
                </p>
              </div>
            </div>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
              <!-- Add Sections Button -->
              <button
                @click="navigateToAddSections"
                class="group bg-gradient-to-br from-blue-100 to-blue-200 dark:from-blue-900/30 dark:to-blue-800/30 hover:from-blue-200 hover:to-blue-300 dark:hover:from-blue-800/40 dark:hover:to-blue-700/40 border-2 border-blue-300 dark:border-blue-700 hover:border-blue-400 dark:hover:border-blue-600 rounded-xl p-6 transition-all duration-200 shadow-sm hover:shadow-md"
              >
                <div class="flex flex-col items-center space-y-3">
                  <div class="p-4 bg-blue-600 rounded-xl group-hover:bg-blue-700 transition-colors shadow-sm">
                    <Icon name="mdi:puzzle-plus" class="text-white text-2xl" />
                  </div>
                  <div class="text-center">
                    <h4 class="font-semibold text-gray-900 dark:text-white group-hover:text-blue-900 dark:group-hover:text-blue-100 transition-colors text-sm">
                      Add Profile Sections
                    </h4>
                    <p class="text-xs text-gray-700 dark:text-gray-400 mt-2">
                      Add experience, education, skills, and more sections
                    </p>
                  </div>
                </div>
              </button>

              <!-- Extract from Resume Button -->
              <button
                @click="navigateToExtractFromResume"
                class="group bg-gradient-to-br from-green-100 to-green-200 dark:from-green-900/30 dark:to-green-800/30 hover:from-green-200 hover:to-green-300 dark:hover:from-green-800/40 dark:hover:to-green-700/40 border-2 border-green-300 dark:border-green-700 hover:border-green-400 dark:hover:border-green-600 rounded-xl p-6 transition-all duration-200 shadow-sm hover:shadow-md"
              >
                <div class="flex flex-col items-center space-y-3">
                  <div class="p-4 bg-green-600 rounded-xl group-hover:bg-green-700 transition-colors shadow-sm">
                    <Icon name="mdi:file-document-plus" class="text-white text-2xl" />
                  </div>
                  <div class="text-center">
                    <h4 class="font-semibold text-gray-900 dark:text-white group-hover:text-green-900 dark:group-hover:text-green-100 transition-colors text-sm">
                      Extract from Resume
                    </h4>
                    <p class="text-xs text-gray-700 dark:text-gray-400 mt-2">
                      Upload your existing resume and extract information
                    </p>
                  </div>
                </div>
              </button>

              <!-- Extract from LinkedIn Button -->
              <button
                @click="navigateToExtractFromLinkedIn"
                class="group bg-gradient-to-br from-indigo-100 to-indigo-200 dark:from-indigo-900/30 dark:to-indigo-800/30 hover:from-indigo-200 hover:to-indigo-300 dark:hover:from-indigo-800/40 dark:hover:to-indigo-700/40 border-2 border-indigo-300 dark:border-indigo-700 hover:border-indigo-400 dark:hover:border-indigo-600 rounded-xl p-6 transition-all duration-200 shadow-sm hover:shadow-md"
              >
                <div class="flex flex-col items-center space-y-3">
                  <div class="p-4 bg-indigo-600 rounded-xl group-hover:bg-indigo-700 transition-colors shadow-sm">
                    <Icon name="mdi:linkedin" class="text-white text-2xl" />
                  </div>
                  <div class="text-center">
                    <h4 class="font-semibold text-gray-900 dark:text-white group-hover:text-indigo-900 dark:group-hover:text-indigo-100 transition-colors text-sm">
                      Import LinkedIn Profile
                    </h4>
                    <p class="text-xs text-gray-700 dark:text-gray-400 mt-2">
                      Connect and import your professional LinkedIn data
                    </p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>

        <!-- Step 2: Job Input -->
        <div class="relative">
          <div class="absolute -left-4 top-8 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-bold z-10">
            2
          </div>
          <JobInputCard @job-analyzed="handleJobAnalyzed" />
        </div>

        <!-- Step 3: Resume Generation Results -->
        <div v-if="currentJob" class="relative">
          <div class="absolute -left-4 top-8 w-8 h-8 bg-green-600 text-white rounded-full flex items-center justify-center text-sm font-bold z-10">
            3
          </div>
          
          <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-300 dark:border-gray-700 p-6">
            <div class="flex items-center mb-4">
              <div class="p-3 bg-green-100 dark:bg-green-900/30 rounded-full mr-4">
                <Icon name="mdi:check-circle" class="text-2xl text-green-700 dark:text-green-400" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                  Resume Generated Successfully!
                </h3>
                <p class="text-sm text-gray-600 dark:text-gray-400">
                  {{ currentJob.matchPercentage }}% match for {{ currentJob.title }} at {{ currentJob.company }}
                </p>
              </div>
            </div>
            
            <!-- Generated Resume Preview -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div class="space-y-4">
                <h4 class="font-medium text-gray-900 dark:text-white">Key Highlights</h4>
                <ul class="space-y-2">
                  <li
                    v-for="highlight in currentJob.highlights"
                    :key="highlight"
                    class="flex items-start text-sm text-gray-700 dark:text-gray-300"
                  >
                    <Icon name="mdi:check" class="text-green-500 mr-2 mt-0.5 flex-shrink-0" />
                    {{ highlight }}
                  </li>
                </ul>
              </div>
              
              <div class="space-y-4">
                <h4 class="font-medium text-gray-900 dark:text-white">Skills Emphasized</h4>
                <div class="flex flex-wrap gap-2">
                  <span
                    v-for="skill in currentJob.emphasizedSkills"
                    :key="skill"
                    class="px-3 py-1.5 bg-blue-200 dark:bg-blue-900/30 text-blue-900 dark:text-blue-300 text-xs font-medium rounded-full border border-blue-300 dark:border-blue-700"
                  >
                    {{ skill }}
                  </span>
                </div>
              </div>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex justify-end space-x-3 mt-6">
              <button
                class="px-4 py-2 bg-gray-200 hover:bg-gray-300 dark:bg-gray-700 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-300 rounded-lg transition-colors font-medium border border-gray-300 dark:border-gray-600"
                @click="previewResume"
              >
                <Icon name="mdi:eye" class="mr-2" />
                Preview
              </button>
              <button
                class="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors font-medium shadow-sm"
                @click="downloadResume"
              >
                <Icon name="mdi:download" class="mr-2" />
                Download PDF
              </button>
              <button
                class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors font-medium shadow-sm"
                @click="saveResume"
              >
                <Icon name="mdi:content-save" class="mr-2" />
                Save Resume
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Right Column - Recent Resumes & Tips -->
      <div class="space-y-8">
        <!-- Recent Resumes -->
        <ResumePreviewCard
          @create-resume="scrollToJobInput"
          @select-resume="handleResumeSelect"
        />

        <!-- Quick Tips -->
        <div class="bg-white dark:bg-gray-800 rounded-xl shadow-md border border-gray-300 dark:border-gray-700 p-6">
          <div class="flex items-center mb-4">
            <div class="p-3 bg-yellow-100 dark:bg-yellow-900/30 rounded-lg mr-3">
              <Icon name="mdi:lightbulb" class="text-yellow-700 dark:text-yellow-400 text-lg" />
            </div>
            <h3 class="font-semibold text-gray-900 dark:text-white">Quick Tips</h3>
          </div>
          
          <div class="space-y-3 text-sm text-gray-700 dark:text-gray-400">
            <div class="flex items-start">
              <Icon name="mdi:check" class="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Paste the complete job description for better AI analysis</span>
            </div>
            <div class="flex items-start">
              <Icon name="mdi:check" class="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Keep your profile updated for more accurate matches</span>
            </div>
            <div class="flex items-start">
              <Icon name="mdi:check" class="text-green-600 mr-2 mt-0.5 flex-shrink-0" />
              <span>Review and customize generated resumes before applying</span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Resume Preview Modal -->
    <!-- <ResumeModal
      v-if="showResumeModal"
      :resume="selectedResume"
      @close="showResumeModal = false"
    /> -->
  </div>
</template>
