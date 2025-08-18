<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow duration-200">
    <!-- Header -->
    <div class="flex items-center mb-4">
      <div class="p-3 bg-blue-50 dark:bg-blue-900/30 rounded-full mr-4">
        <Icon name="mdi:briefcase-search" class="text-2xl text-blue-600 dark:text-blue-400" />
      </div>
      <div>
        <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
          Paste Job Description
        </h3>
        <p class="text-sm text-gray-600 dark:text-gray-400">
          Start by pasting the job you want to apply for
        </p>
      </div>
    </div>

    <!-- Job Input Form -->
    <div class="space-y-4">
      <!-- Company & Job Title -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label for="company" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Company Name
          </label>
          <input
            id="company"
            v-model="company"
            type="text"
            placeholder="e.g., Google, Apple, Microsoft"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          />
        </div>
        <div>
          <label for="jobTitle" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Job Title
          </label>
          <input
            id="jobTitle"
            v-model="jobTitle"
            type="text"
            placeholder="e.g., Software Engineer, Marketing Manager"
            class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400"
          />
        </div>
      </div>

      <!-- Job Description Textarea -->
      <div>
        <label for="jobDescription" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Description
        </label>
        <textarea
          id="jobDescription"
          v-model="jobDescription"
          rows="8"
          placeholder="Paste the full job description here..."
          class="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 dark:focus:ring-blue-400 dark:focus:border-blue-400 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 resize-none"
          @input="handleJobDescriptionInput"
        />
        <div class="flex justify-between items-center mt-2">
          <p class="text-xs text-gray-500 dark:text-gray-400">
            {{ characterCount }} characters
          </p>
          <div v-if="isAnalyzing" class="flex items-center text-blue-600 dark:text-blue-400">
            <Icon name="mdi:loading" class="animate-spin mr-1 text-sm" />
            <span class="text-xs">Analyzing...</span>
          </div>
        </div>
      </div>

      <!-- Quick Analysis Preview (if job description exists) -->
      <div v-if="keyRequirements.length > 0" class="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-4">
        <h4 class="text-sm font-medium text-gray-900 dark:text-white mb-2">
          Key Requirements Detected
        </h4>
        <div class="flex flex-wrap gap-2">
          <span
            v-for="requirement in keyRequirements.slice(0, 6)"
            :key="requirement"
            class="px-2 py-1 bg-blue-100 dark:bg-blue-900/30 text-blue-800 dark:text-blue-300 text-xs rounded-full"
          >
            {{ requirement }}
          </span>
          <span
            v-if="keyRequirements.length > 6"
            class="px-2 py-1 bg-gray-100 dark:bg-gray-600 text-gray-600 dark:text-gray-400 text-xs rounded-full"
          >
            +{{ keyRequirements.length - 6 }} more
          </span>
        </div>
      </div>

      <!-- Action Button -->
      <div class="flex justify-end">
        <button
          :disabled="!canProceed"
          class="px-6 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 dark:disabled:bg-gray-600 text-white font-medium rounded-lg transition-colors disabled:cursor-not-allowed"
          @click="handleAnalyzeJob"
        >
          <Icon v-if="isProcessing" name="mdi:loading" class="animate-spin mr-2" />
          {{ isProcessing ? 'Processing...' : 'Analyze Job & Create Resume' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
// Form data
const company = ref<string>('')
const jobTitle = ref<string>('')
const jobDescription = ref<string>('')
const keyRequirements = ref<string[]>([])

// States
const isAnalyzing = ref<boolean>(false)
const isProcessing = ref<boolean>(false)

// Computed
const characterCount = computed(() => jobDescription.value.length)
const canProceed = computed(() => 
  company.value.trim() && 
  jobTitle.value.trim() && 
  jobDescription.value.trim().length > 100
)

// Basic keyword extraction (simple implementation for now)
const extractKeyRequirements = (text: string): string[] => {
  const skillKeywords = [
    'javascript', 'python', 'react', 'vue', 'angular', 'node', 'express',
    'sql', 'nosql', 'mongodb', 'postgresql', 'mysql', 'redis',
    'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'git',
    'agile', 'scrum', 'leadership', 'management', 'communication',
    'bachelor', 'master', 'degree', 'certification'
  ]
  
  const lowerText = text.toLowerCase()
  const found = skillKeywords.filter(keyword => lowerText.includes(keyword))
  
  // Add some common phrases detection
  const phrases = []
  if (lowerText.includes('years of experience')) phrases.push('Experience Required')
  if (lowerText.includes('remote')) phrases.push('Remote Work')
  if (lowerText.includes('full-time')) phrases.push('Full-time')
  if (lowerText.includes('startup')) phrases.push('Startup Environment')
  
  return [...new Set([...found, ...phrases])].slice(0, 10)
}

// Debounced analysis
let analysisTimeout: NodeJS.Timeout
const handleJobDescriptionInput = () => {
  if (analysisTimeout) clearTimeout(analysisTimeout)
  
  if (jobDescription.value.length > 50) {
    isAnalyzing.value = true
    analysisTimeout = setTimeout(() => {
      keyRequirements.value = extractKeyRequirements(jobDescription.value)
      isAnalyzing.value = false
    }, 1000)
  } else {
    keyRequirements.value = []
    isAnalyzing.value = false
  }
}

// Handle job analysis and resume creation
const handleAnalyzeJob = async () => {
  if (!canProceed.value) return
  
  isProcessing.value = true
  
  try {
    // TODO: Implement job analysis and resume generation
    // This will integrate with your AI service
    console.log('Analyzing job:', {
      company: company.value,
      jobTitle: jobTitle.value,
      description: jobDescription.value,
      requirements: keyRequirements.value
    })
    
    // Simulate processing time
    await new Promise(resolve => setTimeout(resolve, 2000))
    
    // Navigate to resume generation or show results
    // This will be implemented when we have the resume generation flow
    
  } catch (error) {
    console.error('Error analyzing job:', error)
    // Handle error - show toast or error message
  } finally {
    isProcessing.value = false
  }
}
</script>
