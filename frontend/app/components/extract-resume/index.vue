<script setup lang="ts">
import { ref, computed } from 'vue'
import { resumeService } from '~/services/resumeService'
import { profileService } from '~/services/profileService'
import { useProfileStore } from '~/stores/profileStore'
import type { ResumeImportResponse } from '~/types/resume'

const profileStore = useProfileStore()

const isDragging = ref(false)
const isUploading = ref(false)
const isConfirming = ref(false)
const uploadProgress = ref(0)
const error = ref<string | null>(null)
const selectedFile = ref<File | null>(null)
const uploadResult = ref<ResumeImportResponse | null>(null)
const activeProfile = computed(() => profileStore.activeProfile.value)

// Simulate smooth progress while the real request is in-flight
let progressInterval: ReturnType<typeof setInterval> | null = null

const startProgressSimulation = () => {
  uploadProgress.value = 0
  progressInterval = setInterval(() => {
    if (uploadProgress.value < 85) {
      uploadProgress.value += Math.random() * 8
    }
  }, 400)
}

const stopProgressSimulation = (success: boolean) => {
  if (progressInterval) {
    clearInterval(progressInterval)
    progressInterval = null
  }
  uploadProgress.value = success ? 100 : 0
}

// ── file selection ──────────────────────────────────────────────────────────

const handleFileSelect = (event: Event) => {
  const target = event.target as HTMLInputElement
  if (target.files?.[0]) processFile(target.files[0])
}

const handleDrop = (event: DragEvent) => {
  isDragging.value = false
  const file = event.dataTransfer?.files[0]
  if (file?.type === 'application/pdf') {
    processFile(file)
  } else {
    error.value = 'Please upload a valid PDF file.'
  }
}

const processFile = (file: File) => {
  error.value = null
  uploadResult.value = null
  selectedFile.value = file
}

const removeFile = () => {
  selectedFile.value = null
  uploadProgress.value = 0
  uploadResult.value = null
  error.value = null
}

// ── upload ──────────────────────────────────────────────────────────────────

const handleUpload = async () => {
  if (!selectedFile.value) return

  if (!activeProfile.value?.uuid) {
    error.value = 'No active profile found. Please create a profile first.'
    return
  }

  isUploading.value = true
  error.value = null
  startProgressSimulation()

  try {
    if (!activeProfile.value) throw new Error("No active profile")
    const result = await resumeService.uploadResume(activeProfile.value.uuid, selectedFile.value)
    stopProgressSimulation(true)
    uploadResult.value = result
    // We don't redirect yet! We wait for confirmation.
  } catch (err: any) {
    stopProgressSimulation(false)
    const msg =
      err?.data?.detail ||
      err?.message ||
      'Upload failed. Please try again or fill your profile manually.'
    error.value = msg
  } finally {
    isUploading.value = false
  }
}

// ── confirmation ────────────────────────────────────────────────────────────

const handleConfirm = async (confirm: boolean) => {
  if (!uploadResult.value?.resume_id) return
  
  isConfirming.value = true
  error.value = null
  
  try {
    if (confirm) {
      await resumeService.confirmImport(uploadResult.value.resume_id)
      // Refresh profile data to show newly imported sections
      await profileService.fetchUserProfiles()
      navigateTo('/profile')
    } else {
      await resumeService.rejectImport(uploadResult.value.resume_id)
      // Discard and reset
      removeFile()
    }
  } catch (err: any) {
    error.value = 'Failed to process confirmation. Please try again.'
  } finally {
    isConfirming.value = false
  }
}

// ── helpers ──────────────────────────────────────────────────────────────────

const fileSizeMB = computed(() =>
  selectedFile.value ? (selectedFile.value.size / 1024 / 1024).toFixed(2) : '0'
)

const uploadProgressRounded = computed(() => Math.min(Math.round(uploadProgress.value), 100))

const extractedSummary = computed(() => {
  const d = uploadResult.value?.extracted_data
  if (!d) return null
  return {
    name: d.contact_info?.name,
    email: d.contact_info?.email,
    education: d.education?.length ?? 0,
    experience: d.work_experiences?.length ?? 0,
    skills: d.skills?.length ?? 0,
    projects: d.projects?.length ?? 0,
  }
})
</script>

<template>
  <div class="min-h-screen bg-gray-100 dark:bg-gray-900 py-8">
    <div class="mx-auto px-4 sm:px-6 lg:px-8 max-w-4xl">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow-md border border-gray-300 dark:border-gray-700 p-8">

        <!-- Header -->
        <div class="mb-8">
          <button @click="navigateTo('/profile')" class="text-blue-600 hover:underline mb-4 inline-flex items-center gap-2">
            <span>←</span> Back to Profile
          </button>
          <h1 class="text-3xl font-bold text-gray-900 dark:text-gray-100">Extract from Resume</h1>
          <p class="text-gray-600 dark:text-gray-400 mt-2">
            Upload your PDF resume and our AI will automatically populate your profile fields.
          </p>
        </div>

        <!-- Error banner -->
        <div v-if="error" class="mb-6 p-4 bg-red-100 dark:bg-red-900/30 border border-red-300 dark:border-red-700 text-red-700 dark:text-red-300 rounded-lg flex items-start gap-3">
          <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01M10.293 5.293a1 1 0 011.414 0L21 14.586A2 2 0 0119.586 21H4.414A2 2 0 013 19.586L12.293 5.293z"/>
          </svg>
          <span>{{ error }}</span>
        </div>

        <!-- 1. Drop zone (no file selected yet) -->
        <div
          v-if="!selectedFile && !uploadResult"
          @dragover.prevent="isDragging = true"
          @dragleave.prevent="isDragging = false"
          @drop.prevent="handleDrop"
          :class="[
            'border-2 border-dashed rounded-xl p-12 text-center transition-colors',
            isDragging
              ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
              : 'border-gray-300 dark:border-gray-700 hover:border-blue-400 dark:hover:border-blue-500'
          ]"
        >
          <div class="flex flex-col items-center">
            <div class="bg-blue-100 dark:bg-blue-900/40 p-4 rounded-full mb-4">
              <svg class="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
            </div>
            <p class="text-lg font-medium text-gray-900 dark:text-gray-100">Click to upload or drag and drop</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 mt-1">PDF format only · Max 10 MB</p>
            <input
              type="file"
              class="hidden"
              id="fileInput"
              accept=".pdf"
              @change="handleFileSelect"
            />
            <label
              for="fileInput"
              class="mt-6 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium cursor-pointer transition"
            >
              Select File
            </label>
          </div>
        </div>

        <!-- 2. File selected & Uploading state -->
        <div v-else-if="selectedFile && !uploadResult" class="space-y-6">
          <div class="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg border border-gray-200 dark:border-gray-600">
            <div class="flex items-center gap-4">
              <div class="p-2 bg-red-100 text-red-600 rounded">
                <span class="font-bold text-xs">PDF</span>
              </div>
              <div>
                <p class="font-medium text-gray-900 dark:text-gray-100 truncate max-w-[200px] sm:max-w-md">
                  {{ selectedFile.name }}
                </p>
                <p class="text-xs text-gray-500">{{ fileSizeMB }} MB</p>
              </div>
            </div>
            <button @click="removeFile" :disabled="isUploading" class="text-gray-400 hover:text-red-500 transition disabled:opacity-40">
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>

          <div v-if="isUploading" class="space-y-2">
            <div class="flex justify-between text-sm mb-1">
              <span class="text-blue-600 font-medium">Extracting data with AI…</span>
              <span class="text-gray-500">{{ uploadProgressRounded }}%</span>
            </div>
            <div class="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div
                class="bg-blue-600 h-2 rounded-full transition-all duration-500"
                :style="{ width: uploadProgressRounded + '%' }"
              />
            </div>
            <p class="text-xs text-gray-500 italic">This may take 10-30 seconds as the AI analyses your experience.</p>
          </div>

          <div v-else class="flex justify-end gap-3">
            <button @click="removeFile" class="px-6 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition">
              Change File
            </button>
            <button
              @click="handleUpload"
              class="px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold shadow-md transition"
            >
              Start Extraction
            </button>
          </div>
        </div>

        <!-- 3. Review & Confirmation state -->
        <div v-else-if="uploadResult" class="space-y-6">
          <div class="p-6 bg-green-50 dark:bg-green-900/10 border border-green-200 dark:border-green-800 rounded-xl">
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 bg-green-100 dark:bg-green-800 text-green-600 dark:text-green-300 rounded-full">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h2 class="text-xl font-bold text-gray-900 dark:text-gray-100">Review Extracted Data</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
              <!-- Summary Card -->
              <div class="space-y-4">
                <div v-if="extractedSummary?.name || extractedSummary?.email" class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-2">Contact Info</h3>
                  <p v-if="extractedSummary?.name" class="text-lg font-bold text-gray-900 dark:text-gray-100">{{ extractedSummary.name }}</p>
                  <p v-if="extractedSummary?.email" class="text-sm text-gray-600 dark:text-gray-400">{{ extractedSummary.email }}</p>
                </div>

                <div class="bg-white dark:bg-gray-800 p-4 rounded-lg shadow-sm border border-gray-200 dark:border-gray-700">
                  <h3 class="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-3">Extracted Sections</h3>
                  <div class="space-y-2">
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 dark:text-gray-400">Education</span>
                      <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-bold rounded">{{ extractedSummary?.education }}</span>
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 dark:text-gray-400">Experience</span>
                      <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-bold rounded">{{ extractedSummary?.experience }}</span>
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 dark:text-gray-400">Skills</span>
                      <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-bold rounded">{{ extractedSummary?.skills }}</span>
                    </div>
                    <div class="flex justify-between items-center">
                      <span class="text-gray-600 dark:text-gray-400">Projects</span>
                      <span class="px-2 py-0.5 bg-blue-100 text-blue-700 text-xs font-bold rounded">{{ extractedSummary?.projects }}</span>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Message -->
              <div class="flex flex-col justify-center p-4">
                <p class="text-gray-700 dark:text-gray-300 mb-4">
                  The AI has successfully parsed your resume. Please confirm if you would like to apply these changes to your profile.
                </p>
                <div class="p-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg text-xs text-amber-800 dark:text-amber-300 italic">
                  Note: This will add new entries to your profile. You can still edit or remove them later.
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="mt-8 flex justify-end gap-3 border-t border-green-200 dark:border-green-800 pt-6">
              <button
                @click="handleConfirm(false)"
                :disabled="isConfirming"
                class="px-6 py-2 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition disabled:opacity-50"
              >
                Discard
              </button>
              <button
                @click="handleConfirm(true)"
                :disabled="isConfirming"
                class="px-8 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-bold shadow-lg transition flex items-center gap-2 disabled:opacity-50"
              >
                <span v-if="isConfirming" class="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin"></span>
                Apply to Profile
              </button>
            </div>
          </div>
        </div>

        <!-- Tips -->
        <div v-if="!uploadResult" class="mt-12 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div class="p-4 rounded-lg bg-indigo-50 dark:bg-indigo-900/20 border border-indigo-100 dark:border-indigo-800">
            <h3 class="font-semibold text-indigo-900 dark:text-indigo-300 flex items-center gap-2">
              <span>💡</span> Tip
            </h3>
            <p class="text-sm text-indigo-800 dark:text-indigo-400 mt-1">
              For best results, ensure your PDF is text-searchable and not a scanned image.
            </p>
          </div>
          <div class="p-4 rounded-lg bg-amber-50 dark:bg-amber-900/20 border border-amber-100 dark:border-amber-800">
            <h3 class="font-semibold text-amber-900 dark:text-amber-300 flex items-center gap-2">
              <span>🔒</span> Privacy
            </h3>
            <p class="text-sm text-amber-800 dark:text-amber-400 mt-1">
              Your files are processed securely and used only to populate your profile.
            </p>
          </div>
        </div>

      </div>
    </div>
  </div>
</template>