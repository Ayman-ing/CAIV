<script setup lang="ts">
// Types
interface Resume {
  id: string
  jobTitle: string
  company: string
  matchPercentage: number
  createdAt: string
  summary?: string
  highlightedSkills?: string[]
  content?: string
  format?: 'pdf' | 'docx' | 'txt'
}

// Emits
const emit = defineEmits<{
  'create-resume': []
  'select-resume': [resume: Resume]
}>()

// State
const viewMode = ref<'grid' | 'list'>('grid')
const isLoadingMore = ref<boolean>(false)
const hasMoreResumes = ref<boolean>(false)

// Mock data - this would come from a store/API
const resumes = ref<Resume[]>([
  {
    id: '1',
    jobTitle: 'Senior Frontend Developer',
    company: 'Google',
    matchPercentage: 92,
    createdAt: '2024-01-15T10:00:00Z',
    summary: 'Tailored for Google\'s emphasis on React and TypeScript skills',
    highlightedSkills: ['React', 'TypeScript', 'Next.js', 'Node.js', 'AWS']
  },
  {
    id: '2',
    jobTitle: 'Full Stack Engineer',
    company: 'Stripe',
    matchPercentage: 88,
    createdAt: '2024-01-14T15:30:00Z',
    summary: 'Highlighted fintech experience and API development',
    highlightedSkills: ['Python', 'PostgreSQL', 'Docker', 'Kubernetes', 'REST APIs']
  },
  {
    id: '3',
    jobTitle: 'Product Manager',
    company: 'Microsoft',
    matchPercentage: 76,
    createdAt: '2024-01-13T09:15:00Z',
    summary: 'Emphasized technical background and product strategy',
    highlightedSkills: ['Product Strategy', 'Agile', 'Data Analysis', 'Leadership']
  }
])

// Methods
const formatDate = (dateString: string): string => {
  const date = new Date(dateString)
  const now = new Date()
  const diffTime = now.getTime() - date.getTime()
  const diffDays = Math.floor(diffTime / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return 'Today'
  if (diffDays === 1) return 'Yesterday'
  if (diffDays < 7) return `${diffDays} days ago`
  
  return date.toLocaleDateString('en-US', { 
    month: 'short', 
    day: 'numeric',
    year: date.getFullYear() !== now.getFullYear() ? 'numeric' : undefined
  })
}

const selectResume = (resume: Resume) => {
  emit('select-resume', resume)
}

const downloadResume = async (resume: Resume) => {
  try {
    // TODO: Implement resume download
    console.log('Downloading resume:', resume.id)
    
    // Simulate download
    const link = document.createElement('a')
    link.href = '#' // This would be the actual file URL
    link.download = `${resume.company}_${resume.jobTitle}_Resume.pdf`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (error) {
    console.error('Error downloading resume:', error)
  }
}

const deleteResume = async (resumeId: string) => {
  if (!confirm('Are you sure you want to delete this resume?')) return
  
  try {
    // TODO: Implement resume deletion
    console.log('Deleting resume:', resumeId)
    
    // Remove from local array
    const index = resumes.value.findIndex(r => r.id === resumeId)
    if (index > -1) {
      resumes.value.splice(index, 1)
    }
  } catch (error) {
    console.error('Error deleting resume:', error)
  }
}

const loadMoreResumes = async () => {
  isLoadingMore.value = true
  
  try {
    // TODO: Implement pagination
    console.log('Loading more resumes...')
    
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    hasMoreResumes.value = false
  } catch (error) {
    console.error('Error loading more resumes:', error)
  } finally {
    isLoadingMore.value = false
  }
}
</script>

<template>
  <div class="bg-white dark:bg-gray-800 rounded-xl shadow-sm border border-gray-200 dark:border-gray-700 p-6 hover:shadow-md transition-shadow duration-200">
    <!-- Header -->
    <div class="flex items-center justify-between mb-4">
      <div class="flex items-center">
        <div class="p-3 bg-green-50 dark:bg-green-900/30 rounded-full mr-4">
          <Icon name="mdi:file-document-edit" class="text-2xl text-green-500 dark:text-green-400" />
        </div>
        <div>
          <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
            Generated Resumes
          </h3>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            {{ resumes.length }} resume{{ resumes.length !== 1 ? 's' : '' }} created
          </p>
        </div>
      </div>
      <div class="flex items-center space-x-2">
        <button
          v-if="resumes.length > 0"
          class="p-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
          @click="viewMode = viewMode === 'grid' ? 'list' : 'grid'"
        >
          <Icon :name="viewMode === 'grid' ? 'mdi:view-list' : 'mdi:view-grid'" />
        </button>
      </div>
    </div>

    <!-- Empty State -->
    <div v-if="resumes.length === 0" class="text-center py-8">
      <div class="p-4 bg-gray-50 dark:bg-gray-700/50 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
        <Icon name="mdi:file-document-plus" class="text-2xl text-gray-400" />
      </div>
      <h4 class="text-lg font-medium text-gray-900 dark:text-white mb-2">
        No resumes yet
      </h4>
      <p class="text-gray-600 dark:text-gray-400 mb-4">
        Paste a job description above to generate your first AI-powered resume
      </p>
      <button
        class="px-4 py-2 bg-purple-600 hover:bg-purple-700 text-white rounded-lg transition-colors"
        @click="$emit('create-resume')"
      >
        Create Your First Resume
      </button>
    </div>

    <!-- Resume List -->
    <div v-else>
      <!-- Grid View -->
      <div v-if="viewMode === 'grid'" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        <div
          v-for="resume in resumes"
          :key="resume.id"
          class="border border-gray-200 dark:border-gray-700 rounded-lg p-4 hover:shadow-md transition-all cursor-pointer group"
          @click="selectResume(resume)"
        >
          <!-- Resume Thumbnail -->
          <div class="aspect-[3/4] bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-600 rounded mb-3 relative overflow-hidden">
            <div class="p-2 text-xs text-gray-500 space-y-1">
              <div class="h-2 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
              <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
              <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded w-5/6"></div>
              <div class="h-1 bg-gray-200 dark:bg-gray-700 rounded w-4/5"></div>
              <div class="mt-2 h-2 bg-blue-300 dark:bg-blue-600 rounded w-1/2"></div>
            </div>
            <div class="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-10 transition-all flex items-center justify-center">
              <Icon name="mdi:eye" class="text-white text-xl opacity-0 group-hover:opacity-100 transition-opacity" />
            </div>
          </div>
          
          <!-- Resume Info -->
          <div class="space-y-2">
            <h4 class="font-medium text-gray-900 dark:text-white truncate">
              {{ resume.jobTitle }} - {{ resume.company }}
            </h4>
            <p class="text-sm text-gray-600 dark:text-gray-400">
              {{ resume.matchPercentage }}% match
            </p>
            <div class="flex items-center justify-between">
              <span class="text-xs text-gray-500 dark:text-gray-400">
                {{ formatDate(resume.createdAt) }}
              </span>
              <div class="flex items-center space-x-1">
                <button
                  class="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  @click.stop="downloadResume(resume)"
                >
                  <Icon name="mdi:download" class="text-sm" />
                </button>
                <button
                  class="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                  @click.stop="deleteResume(resume.id)"
                >
                  <Icon name="mdi:delete" class="text-sm" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- List View -->
      <div v-else class="space-y-3">
        <div
          v-for="resume in resumes"
          :key="resume.id"
          class="flex items-center p-4 border border-gray-200 dark:border-gray-700 rounded-lg hover:shadow-md transition-all cursor-pointer"
          @click="selectResume(resume)"
        >
          <div class="w-12 h-16 bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-600 rounded mr-4 flex-shrink-0">
            <div class="p-1 text-xs text-gray-400 space-y-0.5">
              <div class="h-1 bg-gray-300 dark:bg-gray-600 rounded w-full"></div>
              <div class="h-0.5 bg-gray-200 dark:bg-gray-700 rounded w-full"></div>
              <div class="h-0.5 bg-gray-200 dark:bg-gray-700 rounded w-3/4"></div>
            </div>
          </div>
          
          <div class="flex-grow">
            <div class="flex items-center justify-between mb-1">
              <h4 class="font-medium text-gray-900 dark:text-white">
                {{ resume.jobTitle }} at {{ resume.company }}
              </h4>
              <div class="flex items-center space-x-2">
                <span class="px-2 py-1 bg-green-100 dark:bg-green-900/30 text-green-800 dark:text-green-300 text-xs rounded-full">
                  {{ resume.matchPercentage }}% match
                </span>
                <span class="text-xs text-gray-500 dark:text-gray-400">
                  {{ formatDate(resume.createdAt) }}
                </span>
              </div>
            </div>
            
            <p class="text-sm text-gray-600 dark:text-gray-400 mb-2">
              {{ resume.summary || 'AI-generated resume tailored for this position' }}
            </p>
            
            <div class="flex items-center justify-between">
              <div class="flex flex-wrap gap-1">
                <span
                  v-for="skill in resume.highlightedSkills?.slice(0, 3)"
                  :key="skill"
                  class="px-1.5 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-700 dark:text-blue-300 text-xs rounded"
                >
                  {{ skill }}
                </span>
                <span
                  v-if="resume.highlightedSkills && resume.highlightedSkills.length > 3"
                  class="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 text-xs rounded"
                >
                  +{{ resume.highlightedSkills.length - 3 }}
                </span>
              </div>
              
              <div class="flex items-center space-x-2">
                <button
                  class="p-1 text-gray-400 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
                  @click.stop="downloadResume(resume)"
                >
                  <Icon name="mdi:download" />
                </button>
                <button
                  class="p-1 text-gray-400 hover:text-red-600 dark:hover:text-red-400 transition-colors"
                  @click.stop="deleteResume(resume.id)"
                >
                  <Icon name="mdi:delete" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMoreResumes" class="text-center mt-4">
        <button
          class="px-4 py-2 text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 font-medium"
          @click="loadMoreResumes"
          :disabled="isLoadingMore"
        >
          <Icon v-if="isLoadingMore" name="mdi:loading" class="animate-spin mr-2" />
          {{ isLoadingMore ? 'Loading...' : 'Load More' }}
        </button>
      </div>
    </div>
  </div>
</template>


